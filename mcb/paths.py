import os
from pathlib import Path

FOLDER_OF_THIS_FILE = Path(
    os.path.dirname(
        p=os.path.realpath(
            path=__file__
        )
    )
)

FILEPATH_OF_MCB_LIST_WORD_DOC = FOLDER_OF_THIS_FILE.parent / Path("logs") / Path("mcb_list_holder.docx")
FILEPATH_OF_MCB_RECORD_WORD_DOC = FOLDER_OF_THIS_FILE.parent / Path("logs") / Path("mcb_record_holder.docx")
FILEPATH_OF_MCB_IMG_WORD_DOC = FOLDER_OF_THIS_FILE.parent / Path("logs") / Path("mcb_img_holder.docx")

TO_FOLDER = FOLDER_OF_THIS_FILE.parent / Path("store") / Path("mcb")

TO_RECORD = FOLDER_OF_THIS_FILE.parent / Path("store") / Path("record")