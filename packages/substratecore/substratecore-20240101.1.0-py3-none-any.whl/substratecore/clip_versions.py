from .pydantic_models import CLIPIn, CLIPOut, ErrorOut, CLIPEmbedding
from .versions import ToIn, FromOut
from typing import Dict, Any, Optional, Union, List
from pydantic import ValidationError


class ToCLIPIn(ToIn[CLIPIn]):
    def from_version(self, version: Optional[str]) -> Union[CLIPIn, ErrorOut]:
        versions = {}
        res = self.json
        for date, fn in sorted(versions.items(), key=lambda x: x[0]):
            if version and version < date:
                res = fn(res)

        # Schema-level validation
        model = None
        try:
            model = CLIPIn(**res)
        except ValidationError as e:
            import json

            e_json_str = e.json()
            e_json = json.loads(e_json_str)[0]
            message = f"{e_json.get('msg')}: {e_json.get('loc')}"
            return ErrorOut(type="invalid_request_error", message=message)

        # Additional validation
        ids = [doc.id for doc in model.docs if doc.id]
        metadatas = [doc.metadata for doc in model.docs if doc.metadata]
        embed_metadata_keys_list = [
            doc.embed_metadata_keys for doc in model.docs if doc.embed_metadata_keys
        ]
        texts = [doc.text for doc in model.docs if doc.text]
        image_urls = [doc.image_url for doc in model.docs if doc.image_url]
        if len(model.docs) > 256:
            return ErrorOut(
                type="invalid_request_error",
                message="Max embedding batch size is 256 documents.",
            )
        if model.store and (len(ids) != len(set(ids))):
            dupes = set([i for i in ids if ids.count(i) > 1])
            return ErrorOut(
                type="invalid_request_error",
                message=f"Can't store documents with duplicate ids: {dupes}",
            )

        def validate_metadatas(input):
            if len(metadatas) > 0:
                if len(metadatas) != len(input):
                    return ErrorOut(
                        type="invalid_request_error",
                        message=f"When using metadata all docs must include metadata",
                    )

            if len(embed_metadata_keys_list) > 0 and (
                len(embed_metadata_keys_list) != len(input)
            ):
                return ErrorOut(
                    type="invalid_request_error",
                    message=f"When using embed_metadata_keys all docs must include embed_metadata_keys",
                )
            return None

        error = None
        if len(texts) > 0:
            error = validate_metadatas(texts)
        elif len(image_urls) > 0:
            error = validate_metadatas(image_urls)

        if error is not None:
            return error
        return model


class FromCLIPOut(FromOut[Any]):
    def to_version(self, version: Optional[str]) -> Any:
        versions = {}
        res = self.data
        for date, fn in sorted(versions.items(), key=lambda x: x[0], reverse=True):
            if version and version < date:
                res = fn(res)
        return res
