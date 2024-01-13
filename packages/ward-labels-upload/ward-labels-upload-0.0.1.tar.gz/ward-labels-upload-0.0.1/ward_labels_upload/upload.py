import requests
from tqdm import tqdm

from ward_labels_upload.config import DEFAULT_BASE_URL, LABEL_UPLOAD_ENDPOINT
from ward_labels_upload.domain import Label
from ward_labels_upload.utils import split_into_batches


class LabelUploadFailedException(Exception):
    """ An exception raised when a label upload fails. """
    pass


class LabelUploader:
    """ A class for uploading labels to the Ward Analytics API."""
    
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        self._api_key = api_key
        self._base_url = base_url
        
        
    def _upload_batch(self, labels: list[Label]) -> None:
        """ Uploads a batch of labels to the Ward Analytics API.
        
        Args:
            labels (List[Label]): The batch of labels to upload.
            
        Raises:
            LabelUploadFailedException: If the Ward Analytics API returns an error.
        """
        labels_dict: dict[str, list[str]] = {}
        descriptions_dict: dict[str, list[str]] = {}
        for label in labels:
            if label.address not in labels_dict:
                labels_dict[label.address] = []
            labels_dict[label.address].append(label.label)
            
            if label.address not in descriptions_dict:
                descriptions_dict[label.address] = []
            descriptions_dict[label.address].append(label.description)
            
        if len(labels_dict) != len(descriptions_dict):
            raise ValueError("The number of labels and descriptions does not match.")
        
        payload = {
            "labels": labels_dict,
            "descriptions": descriptions_dict
        }
        
        headers = {
            "api": self._api_key
        }
        
        response = requests.post(self._base_url + LABEL_UPLOAD_ENDPOINT, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise LabelUploadFailedException("The Ward Analytics API returned an error.")

        
    
    def upload_labels(self, labels: list[Label]) -> None:
        """ Uploads a list of labels to the Ward Analytics API.
        
        If the list of labels is too big, it will be split into multiple upload batches.
        Will display a progress bar.
        
        Args:
            labels (List[Label]): The list of labels to upload.
            
        Raises:
            LabelUploadFailedException: If the Ward Analytics API returns an error.
        """
        BATCH_SIZE = 1000
        
        batches = split_into_batches(labels, BATCH_SIZE)
        for batch in tqdm(batches, unit="batch", desc="Uploading labels"):
            self._upload_batch(batch)
        

