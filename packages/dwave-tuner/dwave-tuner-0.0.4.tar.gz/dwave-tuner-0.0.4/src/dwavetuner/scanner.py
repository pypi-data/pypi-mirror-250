import itertools
import logging
import numpy as np
import dimod
import dwave
import dwave.system
from .job import Job
from . import utils


class Scanner:
    """Prepare a set of Jobs that are ready to be sent to a QPU.

    The jobs differ by their solver parameters, which are tuned via grid scan.

    Attributes:
        composites: List containing the different composites. If a fixed
            embedding was passed, then it has a length of 1. Else, it has
            num_embeddings entries.

        bqm: BinaryQuadraticModel that contains the problem formulation at
            hand.

        jobs: Dict that contains the Jobs that were sent to the QPU.

        num_embeddings: The number of embeddings to compare.

        num_reads: Number of samples per Job.

        num_reps: Number of repeated Jobs with identical parameters to obtain
            a sample size of num_reads * num_reps, since each QPU solver limits
            num_reads. To obtain a large enough sample, further reps are
            needed.

        num_chain_strengths: Number of equidistant chain strengths to try out
            in a grid scan.

        num_annealing_times: Number of annealing times to try out in a grid
            scan.

        results: Dict of Results which classify a response's records and count
            the number of optimal or valid samples to determine a success
            probability.

        sampler: This attribute holds the constructed Sampler as a read-only
            property.
    """

    # Settings and objects that all instances use
    sampler = None
    hybrid_sampler = None
    cache_root = 'json_data/'

    def __init__(self, bqm, **kwargs):
        """Prepare the D-Wave system to scan through parameter landscape.

        Args:
            sampler_region: Set an alternate region to find the best QPU.
                Default is 'eu-central-1'.

            embedding: Specify a fixed embedding for this Scanner. As a
                consequence, the num_embeddings class attribute is ignored
                and tuning is done on this specific embedding.
        """
        # Input parameters
        self.sampler_region = kwargs.get('sampler_region', 'eu-central-1')
        self.bqm = bqm

        self.label = kwargs.get('label')

        # Sample size
        self.num_reads = kwargs.get('num_reads', 100)
        self.num_reps = kwargs.get('num_reps', 10)

        # Grid scan
        self.chain_strengths_start = kwargs.get('chain_strengths_start', 0.)
        self.chain_strengths_end = kwargs.get('chain_strengths_end', 1.)
        self.num_chain_strengths = kwargs.get('num_chain_strengths', 1)
        self.num_annealing_times = kwargs.get('num_annealing_times', 1)

        # Fixed chain strength
        if kwargs.get('chain_strength') is not None:
            # Overrides start, end, num chain strengths
            self.chain_strengths_start = kwargs['chain_strength']
            self.chain_strengths_end = kwargs['chain_strength']
            self.num_chain_strengths = 1

        self.alt_sampler = kwargs.get('sampler')

        # Initialize D-Wave system
        if Scanner.hybrid_sampler is None:
            Scanner.hybrid_sampler = dwave.system.LeapHybridSampler()
        if Scanner.sampler is None:
            Scanner.sampler = self._init_sampler()
        self.composites = []

        # Embedding context
        embedding = kwargs.get('embedding')
        if embedding is not None:
            # FixedEmbeddingComposite
            self.num_embeddings = 1
            self._cached_embeddings = [embedding]
            logging.info('Using fixed embedding')
        else:
            self.num_embeddings = kwargs.get('num_embeddings', 10)
            if self.cache_exists and self.alt_sampler is None:
                self._cached_embeddings = self._load_embeddings_from_cache()
            else:
                self._cached_embeddings = []

        self.composites = self._init_composites()

        # Output
        self.jobs = {}

    def __str__(self):
        label = ""

        if self.label is not None:
            label = f'{self.label}/'

        label += f'{self.bqm.num_variables}hs' \
                 f'_{self.bqm.num_interactions}Js' \
                 f'_{self.num_reads}reads' \
                 f'_{self.num_reps}reps' \
                 f'_{self.num_chain_strengths}cs'

        if self.chain_strengths_start != 0.0 or self.chain_strengths_end != 1.0:
            label += f'_{self.chain_strengths_start}-{self.chain_strengths_end}'

        if self.num_annealing_times > 1:
            label += f'_{self.num_annealing_times}at'

        return label

    @property
    def annealing_times(self):
        return 2 * np.logspace(1, 3, num=self.num_annealing_times)

    @property
    def cache_directory(self):
        """Cache directory for this scan."""
        return Scanner.cache_root + self.__str__()

    @property
    def cache_exists(self):
        """If cache_exists(), then we ran this very scan before."""
        return utils.exists(self.cache_directory)

    @property
    def chain_strengths(self):
        """List of chain strengths that are supposed to be scanned. It has
        a length of num_chain_strengths.
        """
        if self.num_chain_strengths == 1 and self.chain_strengths_start == 0.:
            logging.info('Using None chain strength since 0 is passed.')
            return [None]

        a = self.chain_strengths_start
        b = self.chain_strengths_end
        num = self.num_chain_strengths
        return np.linspace(a + (b - a) / num, b, num=num)

    @property
    def default_chain_strengths(self):
        default_cs = dwave.embedding.chain_strength.uniform_torque_compensation
        return [default_cs(self.bqm, e) / self.qubo_max for e in self.embeddings]

    @property
    def embeddings(self):
        """List of embeddings to re-use for future Scanners and Jobs.

        It has a length of num_embeddings. If a fixed embedding was passed,
        num_embeddings is fixed to 1.
        """
        return [self.composites[i].embedding for i in range(self.num_embeddings)]

    @property
    def num_samples(self):
        """Sample size num_reads * num_reps.

        num_reads is limited depending on the QPU solver picked. To gather more
        statistics, repetitions are needed."""
        return self.num_reads * self.num_reps

    @property
    def params(self):
        """Tuple with optimal tuning parameters.

        (embedding_id, chain_strength, annealing_time)"""
        return max(self.results, key=self.results.get)

    @property
    def qubo(self):
        """Dict containing QUBO coefficients."""
        return self.bqm.to_qubo()[0]

    @property
    def qubo_max(self):
        """Absolute value of QUBO coefficient with the greatest magnitude."""
        return max([abs(value) for value in self.qubo.values()])

    @property
    def response(self):
        """Tuning results summary.

        Returns None until grid_scan() is run.
        """
        response = {}

        # Get embedding_id, chain_strength with the highest success prob.
        embedding_id = self.params[0]
        response['embedding_id'] = embedding_id
        response['chain_strength'] = self.params[1]
        response['annealing_time'] = self.params[2]

        p = self.results[self.params] / self.num_samples
        response['success_probability'] = p

        z = 1.959963984540  # 95 % CI
        response['error'] = z * np.sqrt(p * (1 - p) / self.num_samples)

        if self.alt_sampler is None:
            response['default_chain_strength'] = self.default_chain_strengths[embedding_id]
            response['embedding'] = self.embeddings[embedding_id]

        return response

    @property
    def results(self):
        """Full tuning results.

        Returns None until grid_scan() is run.
        """
        # Aggregate reps
        results = {}
        for old_params, job in self.jobs.items():

            # Do not include rep id in this dict.
            params = old_params[:-1]

            if params not in results:
                results[params] = 0
            results[params] += job.result.num_optimal

        return results

    def scan_results(self, scan_type):
        ys = []
        yerrs = []

        if scan_type == 'chain_strength':
            xs = self.chain_strengths
        elif scan_type == 'annealing_time':
            xs = self.annealing_times
        else:
            return None

        for emb in range(self.num_embeddings):
            ys.append([])
            yerrs.append([])

            for cs in self.chain_strengths:
                for at in self.annealing_times:
                    n = self.num_samples
                    n_opt = self.results[emb, cs, at]
                    p = n_opt / n

                    ys[emb].append(p)
                    yerrs[emb].append(np.sqrt(p * (1 - p) / n))

        return xs, ys, yerrs

    def grid_scan(self):
        """Perform a grid scan according to Scanner instance attributes."""
        # Loop ranges
        embedding_ids = range(self.num_embeddings)
        cs = self.chain_strengths
        at = self.annealing_times
        reps = range(self.num_reps)

        # Grid scan
        for params in itertools.product(embedding_ids, cs, at, reps):
            # Parameters
            embedding_id = params[0]
            kwargs = {
                'chain_strength': params[1],
                'annealing_time': params[2],
                'rep': params[-1]
            }

            job = Job(self, self.bqm, embedding_id, **kwargs)
            self.jobs[params] = job
            job.run()

        # This needs to be done after the Jobs are run
        # Until the Job is sent to QPU, no embedding is constructed since
        # sampler and composite do not make use of the BQM yet.
        self._dump_embeddings_to_cache()

        return self.response

    def _dump_embeddings_to_cache(self):
        """Dump embeddings that have not been read from cache."""
        if self.alt_sampler is not None:
            return

        num_cached = len(self._cached_embeddings)
        num = self.num_embeddings

        # We do not need to write what we just read from cache
        if num > num_cached:
            logging.info(f'Dumping {num - num_cached} embeddings to {self.cache_directory}')

        for i in range(num_cached, num):
            path = f'{self.cache_directory}/{i:02}/embedding.json'
            utils.dump_json(self.embeddings[i], path)

    def _init_composites(self):
        """Construct composites with fixed embedding.

        If an embedding was passed, then num_embeddings is equal to 1 and
        composites will hold a single FixedEmbeddingComposite.

        If an embedding was not passed, re-creates k FixedEmbeddingComposites
        from cache and num_embeddings - k new LazyFixedEmbeddingComposites.

        Newly created composites will have their embeddings cached.
        """
        composites = []
        num_cached_embeddings = len(self._cached_embeddings)

        if self.alt_sampler == 'random':
            return [dimod.RandomSampler()]

        if self.alt_sampler == 'exact':
            return [dimod.ExactSolver()]

        if self.alt_sampler == 'simulated':
            return [dimod.SimulatedAnnealingSampler()]

        if self.alt_sampler == 'hybrid':
            return [Scanner.hybrid_sampler]

        for i in range(self.num_embeddings):

            # We want to re-use available cached embedding responses
            if i < num_cached_embeddings:
                # Use fixed embedding from cache
                composite = dwave.system.FixedEmbeddingComposite(
                    Scanner.sampler,
                    embedding=self._cached_embeddings[i]
                )

            else:
                # Create new composite with fresh embedding until
                # num_embeddings composites exist
                composite = dwave.system.LazyFixedEmbeddingComposite(Scanner.sampler)

            composites.append(composite)

        return composites

    def _init_sampler(self):
        """Construct DWaveSampler from region."""
        return dwave.system.DWaveSampler(region=self.sampler_region)

    def _load_embeddings_from_cache(self):
        """Search cache_directory for cached embeddings and load them."""
        embeddings = []
        embedding_paths = utils.ls(self.cache_directory)

        for path in embedding_paths:
            # Hidden files such as .DS_Store
            if path.name[0] == '.':
                continue

            embedding = utils.load_json(str(path) + '/embedding.json')
            embeddings.append(embedding)

        logging.info(f'Loading {len(embeddings)} cached embeddings from {self.cache_directory}')

        return embeddings
