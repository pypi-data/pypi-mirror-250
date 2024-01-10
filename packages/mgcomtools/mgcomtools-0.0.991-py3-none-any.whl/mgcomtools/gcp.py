from google.cloud import storage
storage_client = storage.Client()


class GcsFiles:

    def __init__(self, source=None, destination=None, method='copy'):
        
        self.source_bucket, self.source_blob = self.prepare_link(source)
        self.method = method
        if destination:
            self.destination_bucket, self.destination_blob = self.prepare_link(destination)
            
        if method == 'copy':
            self.copy()
        elif method == 'move':
            self.remove()
        elif method == 'delete':
            self.delete()
            
            
    def prepare_link(self, path):
        
        parsed_path = path.replace('gs://', '').split('/')
        bucket_name = parsed_path[0]
        blob_name = '/'.join(parsed_path[1:])
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        return bucket, blob
        
    
    def copy(self):
        
        status = f"{self.method}:\n{self.source_blob.name}\n===>\n{self.destination_blob.name}"
        print(status)
        rewrite_token = ''
        while rewrite_token is not None:
            rewrite_token, bytes_rewritten, bytes_to_rewrite = self.destination_blob.rewrite(
              self.source_blob, token=rewrite_token)
            print(f'Progress so far: {bytes_rewritten}/{bytes_to_rewrite} bytes.')

            
    def delete(self):

        blobs = self.source_bucket.list_blobs(prefix=self.source_blob.name)
        
        count = 0
        for blob in blobs:
            blob.delete()
            print('deleted:', blob.name)
            count += 1
        
        if count == 0:
            print('No one file has been deleted')
            
            
    def remove(self):
        self.copy()
        self.delete()