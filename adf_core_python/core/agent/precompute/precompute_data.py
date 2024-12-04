import json
import os

ENCODE = "utf-8"


class PrecomputeData:
    def __init__(self, file_path: str) -> None:
        """
        Initialize the PrecomputeData object.

        Parameters
        ----------
        file_path : str
            The path to the precompute data file.

        Raises
        ------
        Exception
        """
        self._precompute_data = self.read_json_data()
        self._file_path = file_path

    def read_json_data(self) -> dict:
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

        with open(self._file_path, "r", encoding=ENCODE) as file:
            return json.load(file)

    def write_json_data(self, data: dict) -> None:
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

        with open(self._file_path, "w", encoding=ENCODE) as file:
            json.dump(data, file, indent=4)

    def remove_precompute_data(self) -> None:
        """
        Remove the precompute data file.
        """
        if os.path.exists(self._file_path):
            os.remove(self._file_path)

    def get_precompute_data(self) -> dict:
        """
        Get the precompute data.

        Returns
        -------
        dict
            The precompute data.
        """
        return self._precompute_data
