class LoopInTreeException(Exception):
    """Raises when a loop is created in family tree."""


class RelationMatchingRequestStatusPriorityError(Exception):
    """Raises when do an action on matching request from invalid status"""
