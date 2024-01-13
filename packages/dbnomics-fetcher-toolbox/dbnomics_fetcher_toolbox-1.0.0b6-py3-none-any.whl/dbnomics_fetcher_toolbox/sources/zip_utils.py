from zipfile import ZipFile


def format_zip_filename(zip_file: ZipFile) -> str:
    return f"(open from {type(zip_file.fp).__name__})" if zip_file.filename is None else repr(zip_file.filename)
