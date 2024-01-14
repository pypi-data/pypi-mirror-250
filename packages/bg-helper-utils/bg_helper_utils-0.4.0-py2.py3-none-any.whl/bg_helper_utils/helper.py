def get_analyis_type() -> str:
    """Get the analysis type.

    Args:
        None

    Returns:
        str: the analysis type

    Raises:
        None
    """
    analysis_type = None
    while analysis_type is None or analysis_type == "":
        analysis_type = input("What is the analysis type? : ")
    return analysis_type.strip()


def get_batch_id() -> str:
    """Get the batch ID type.

    Args:
        None

    Returns:
        str: the batch ID

    Raises:
        None
    """
    batch_id = None
    while batch_id is None or batch_id == "":
        batch_id = input("What is the batch ID? : ")
    return batch_id.strip()

