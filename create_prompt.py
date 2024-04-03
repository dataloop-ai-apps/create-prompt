import dtlpy as dl
import os
import logging

logger = logging.getLogger(name="[CreatePrompt]")


PROMPT_TYPES = {
    "image": dl.PromptType.IMAGE,
    "video": dl.PromptType.VIDEO,
    "audio": dl.PromptType.AUDIO
    }


class ServiceRunner(dl.BaseServiceRunner):
    @staticmethod
    def create_prompt_from_item(item: dl.Item,
                                prompt_text: str = None,
                                combine_texts: bool = True,
                                directory: str = "/.dataloop/prompts") -> dl.Item:
        prompt_name = f"prompt_{os.path.splitext(item.name)[0]}"
        prompt_item = dl.PromptItem(name=prompt_name)
        prompt = dl.Prompt(key="prompt_from_item")
        if 'text' in item.mimetype:
            text = item.download(save_locally=False).read().decode("utf-8")
            if prompt_text and combine_texts:
                text = f"{prompt_text} {text}"
            else:
                logger.warning("Failed to combine text item input with prompt. Using just text item input.")
            prompt.add(mimetype=dl.PromptType.TEXT, value=text)
        elif 'image' in item.mimetype or 'video' in item.mimetype or 'audio' in item.mimetype:
            prompt_type = PROMPT_TYPES[item.mimetype.split("/")[0]]
            value = item.stream
            prompt.add(mimetype=prompt_type, value=value)
            if prompt_text:
                prompt.add(mimetype=dl.PromptType.TEXT, value=prompt_text)
        else:
            raise TypeError(f"Item {item.id} is of type {item.mimetype}, "
                            f"which is currently not supported in prompt items.")
        prompt_item.add(prompt)
        output_item = item.dataset.items.upload(prompt_item, overwrite=True, remote_path=directory)
        output_item.metadata["original_item"] = item.metadata["original_item"] if item.metadata.get("original_item") \
            else item.id
        output_item = output_item.update()
        logger.info(f"Created prompt item {output_item.id} from input item {item.id} at directory {directory} in "
                    f"dataset {item.dataset.name}")
        return output_item

    @staticmethod
    def create_prompt_from_text_annotations(item: dl.Item,
                                            prompt_text: str = None,
                                            combine_texts: bool = True,
                                            directory: str = "/.dataloop/prompts"
                                            ) -> dl.Item:
        text_annotations_filter = dl.Filters("type", "text", resource=dl.FiltersResource.ANNOTATION)
        text_annotations = item.annotations.list(filter=text_annotations_filter)
        if len(text_annotations) > 0:
            if prompt_text and combine_texts:
                text = prompt_text
            else:
                logger.warning("Failed to combine text item input with prompt. Using just text item input.")
                text = ''
            for ann in text_annotations:
                text += f" {ann.coordinates}"
            prompt_name = f"prompt_{os.path.splitext(item.name)[0]}"
            prompt_item = dl.PromptItem(name=prompt_name)
            prompt = dl.Prompt(key="prompt_from_annotations")
            prompt.add(mimetype=dl.PromptType.TEXT, value=text)
            prompt_item.add(prompt)
            output_item = item.dataset.items.upload(prompt_item, overwrite=True, remote_path=directory)
            logger.info(f"Created prompt item {output_item.id} from input item {item.id} at directory {directory} in "
                        f"dataset {item.dataset.name}")
            output_item.metadata["original_item"] = item.metadata["original_item"] if \
                item.metadata.get("original_item") else item.id
            output_item = output_item.update()
            return output_item
        else:
            raise Exception(f"Item {item.id} has no text annotations")
