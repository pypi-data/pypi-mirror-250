from typing import List

from src.hubrdvmairie.models.editor_panorama import EditorPanorama

from ..crud.crud_editor_panorama import editorPanorama as crud
from ..db.postgresdb import session


def get_all_editorPanorama() -> List[EditorPanorama]:
    return crud.get_all(session)
