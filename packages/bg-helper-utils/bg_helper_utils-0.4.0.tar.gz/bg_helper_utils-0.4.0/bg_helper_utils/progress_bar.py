from rich.progress import Progress
from typing import Any, Callable, List

def show_progress_bar(
    func: Callable[[str], None],
    desc: str,
    advance: int = 1,
    items: List[Any] = None
    ) -> None:
    """Display a progress bar to show progress of a function.

    Args:
        func (Callable[[str], None]): The function to be called.
        desc (str): The description of the progress bar.
        advance (int, optional): The number of increments to advance the progress bar by. Defaults to 1.
        items (List[Any], optional): The list of items to be processed. Defaults to None.
    """
    with Progress() as progress:
        task = progress.add_task(f"[cyan]{desc}", total=len(items))

        for item in items:
            # Simulate processing the file (replace this with your actual processing logic)
            func(item)

            # Update the progress bar
            progress.update(task, advance=advance)

