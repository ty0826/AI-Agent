from ipywidgets import FileUpload
from IPython.display import display

upload = FileUpload(accept='image/*', multipart=False)
display(upload)
