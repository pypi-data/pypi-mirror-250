import dimod
from . import utils


class Result:
    """A Result is a container for a Job's response statistics supplying
    evaluation or validation metric.

    Instance results are read-only. If you want to change the optimal energy,
    create a new Result.

    Attributes:
        num_optimal: Number of optimal samples in the response.

        num_samples: Number of samples in the response.
    """

    def __init__(self, response, **kwargs):
        """Translate a response to a Result.

        Args:
            response: SampleSet as returned by a D-Wave sampler.

            optimal_energy: Adjusts optimal energy to a value greater than 0 in
                case the best solution is not a root of the penalty function.
        """
        self.response = response
        self.optimal_energy = kwargs.get('optimal_energy', 0)

        # Perform evaluation upon creation
        self.num_optimal = 0
        self.num_samples = 0

        for record in self.response.aggregate().data():
            self.num_samples += record.num_occurrences
            if self._is_optimal(record):
                self.num_optimal += record.num_occurrences

    def _is_optimal(self, record):
        """True if a record in the response is optimal."""
        return record.energy == self.optimal_energy


class Job:
    """A Job contains the instructions that are sent to a QPU.

    Attributes:
        bqm: BinaryQuadraticModel to be optimized on a QPU.

        composite: D-Wave composite such as EmbeddingComposite mainly used for
            a minor embedding.

        chain_strength: Relative chain strength in interval (0, 1].

        parameters: Dict containing QPU solver parameters as provided by the
            D-Wave SAPI. Examples are 'num_reads' and 'annealing_time'.

    """

    def __init__(self, scanner, bqm, embedding_id, **kwargs):
        """Prepares a Job that is ready to be sent to a suitable QPU."""

        # Model
        self.bqm = bqm

        # Embedding context
        self.embedding_id = embedding_id
        self.composite = scanner.composites[embedding_id]
        self.chain_strength = kwargs.get('chain_strength')

        # Solver parameters
        self.parameters = {}
        if scanner.alt_sampler not in ["exact", "hybrid"]:
            self.parameters['num_reads'] = scanner.num_reads
        if scanner.alt_sampler is None:
            if kwargs.get('auto_scale') is not None:
                self.parameters['auto_scale'] = kwargs['auto_scale']
            if kwargs.get('annealing_time') is not None:
                self.parameters['annealing_time'] = kwargs['annealing_time']

        # Needed to cache responses
        self.cache_directory = scanner.cache_directory
        self.use_cache = True
        self.rep = kwargs.get('rep', 0)

        # Result
        self.response = None
        self.result = None

    def __str__(self):
        if self.chain_strength is None:
            cs = 'auto'
        else:
            cs = f'{self.chain_strength:.3f}'
        label = f"{self.bqm.num_variables}h" \
                f"_{self.bqm.num_interactions}J" \
                f"_Qmax={self.qubo_max}" \
                f"_reads={self.parameters.get('num_reads', 1)}" \
                f"_cs={cs}"

        if 'annealing_time' in self.parameters:
            label += f"_at={self.parameters['annealing_time']}"

        label += f"_{self.rep}"

        return label

    @property
    def abs_chain_strength(self):
        """Converts relative chain_strength from interval (0, 1] to absolute
        chain strength that depends on the magnitude of the QUBO coefficients.
        """
        if self.chain_strength is None:
            return None
        else:
            # TODO Perhaps some rounding could be good here
            return self.qubo_max * self.chain_strength

    @property
    def cache_exists(self):
        """True if a cached response of this Job already exists."""
        return utils.exists(self.cache_path)

    @property
    def cache_path(self):
        """Path to JSON file supposed to hold this Job's past response."""
        return f'{self.cache_directory}/{self.embedding_id:02}/' \
               f'{self.__str__()}.json'

    @property
    def qubo(self):
        """Dict containing QUBO coefficients."""
        return self.bqm.to_qubo()[0]

    @property
    def qubo_max(self):
        """Absolute value of QUBO coefficient with the greatest magnitude."""
        return max([abs(value) for value in self.qubo.values()])

    def run(self):
        """Send Job to QPU and initiate post-processing."""
        self._load_response_from_cache() or self._send()
        self.result = Result(self.response)

    def _dump_response_to_cache(self):
        """Cache response."""
        return utils.dump_json(self.response.to_serializable(), self.cache_path)

    def _load_response_from_cache(self):
        """Re-use response from cache rather than sending to QPU."""
        if self.use_cache and self.cache_exists:

            cached_response = utils.load_json(self.cache_path)
            self.response = dimod.SampleSet.from_serializable(cached_response)

            return True

        else:
            return False

    def _send(self):
        """Send Job to QPU and cache response."""
        params = self.parameters.copy()
        if self.abs_chain_strength is not None:
            params['chain_strength'] = self.abs_chain_strength
        self.response = self.composite.sample(self.bqm, **params)
        self._dump_response_to_cache()
