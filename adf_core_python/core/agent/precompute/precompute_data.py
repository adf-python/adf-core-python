import json
import os

ENCODE = "utf-8"


class PrecomputeData:
    def __init__(self, dir_path: str) -> None:
        """
        Initialize the PrecomputeData object.

        Parameters
        ----------
        dir_path : str
            The directory path to save the precompute data.

        Raises
        ------
        Exception
        """
        self._dir_path = dir_path

    def read_json_data(self, module_name: str) -> dict:
        """
        Read the precompute data from the file.

        Returns
        -------
        dict
            The precompute data.

        Raises
        ------
        Exception
        """

        with open(f"{self._dir_path}/{module_name}.json", "r", encoding=ENCODE) as file:
            return json.load(file)

    def write_json_data(self, data: dict, module_name: str) -> None:
        """
        Write the precompute data to the file.

        Parameters
        ----------
        data : dict
            The data to write.

        Raises
        ------
        Exception
        """
        if not os.path.exists(self._dir_path):
            os.makedirs(self._dir_path)

        with open(f"{self._dir_path}/{module_name}.json", "w", encoding=ENCODE) as file:
            json.dump(data, file, indent=4)

    def remove_precompute_data(self) -> None:
        """
        Remove the precompute data file.
        """
        if os.path.exists(self._dir_path):
            os.remove(self._dir_path)

    def is_available(self) -> bool:
        """
        Check if the precompute data is available.

        Returns
        -------
        bool
            True if the precompute data is available, False otherwise.
        """
        return os.path.exists(self._dir_path)
