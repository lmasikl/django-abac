import collections

from abac.const import NOT_APPLICABLE, INDETERMINATE
from abac.policy_administration_point import AbstractCondition


class PolicySet:
    """ Class describing the basic behavior of the entity "rule" """

    def __init__(self, target, policies, algorithm,
                 obligation=None, advice=None, description=None):
        self.target = target
        self.policies = policies
        self.algorithm = algorithm
        self.obligation = obligation
        self.advice = advice
        self.description = description
        self.error = None
        self.validate_initialization()

    def decision(self):
        if isinstance(self.target, bool):
            target = self.target
        else:
            target = self.target.condition()
        try:
            if target is True:
                return self.algorithm(
                    [policy.decision() for policy in self.policies]
                )
            return NOT_APPLICABLE
        except Exception as e:
            self.error = e
            return INDETERMINATE

    def validate_initialization(self):
        if not isinstance(self.target, (AbstractCondition, bool)):
            raise TypeError('The target is not AbstractCondition or bool')
        if not isinstance(self.policies, collections.Iterable):
            raise TypeError('The policies is not iterable')
        if not callable(self.algorithm):
            raise TypeError('The algorithm is not callable')
        if self.obligation is not None and not callable(self.obligation):
            raise TypeError('The obligation is not callable')
        if self.advice is not None and not callable(self.advice):
            raise TypeError('The advice is not callable')
