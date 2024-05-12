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
                          context: dl.Context) -> dl.Item:

        node = context.node
        prompt_text = node.metadata['customNodeConfig']["prompt_text"]
        combine_texts = node.metadata['customNodeConfig']["combine_texts"]
        prefix = node.metadata['customNodeConfig']["prefix"]
        directory = node.metadata['customNodeConfig']["directory"]

        prompt_name = f"{prefix}-{os.path.splitext(item.name)[0]}"
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
        output_item.metadata["original_item"] = item.metadata.get("original_item", item.id)
        output_item = output_item.update()
        logger.info(f"Created prompt item {output_item.id} from input item {item.id} at directory {directory} in "
                    f"dataset {item.dataset.name}")
        return output_item

    @staticmethod
    def create_prompt_from_item_annotations(item: dl.Item,
                                            context: dl.Context) -> dl.Item:
        node = context.node
        prompt_text = node.metadata['customNodeConfig']["prompt_text"]
        combine_texts = node.metadata['customNodeConfig']["combine_texts"]
        prefix = node.metadata['customNodeConfig']["prefix"]
        directory = node.metadata['customNodeConfig']["directory"]
        annotation_type = node.metadata['customNodeConfig']['annotation_type']

        annotations_filter = dl.Filters('type', annotation_type, use_defaults=False, resource=dl.FiltersResource.ANNOTATION)
        annotations = item.annotations.list(filter=annotations_filter)
        if len(annotations) > 0:
            if prompt_text and combine_texts:
                text = prompt_text
            else:
                logger.warning("Failed to combine text item input with prompt. Using just text item input.")
                text = ''
            if annotation_type == 'text':
                text += " ".join([ann.coordinates for ann in annotations])
            elif annotation_type == 'subtitle':
                text += " ".join([ann.coordinates['text'] for ann in annotations])
            else:
                raise TypeError(f"Annotation of type {annotation_type} is not supported by prompt tools.")
            prompt_name = f"{prefix}-{os.path.splitext(item.name)[0]}"
            prompt_item = dl.PromptItem(name=prompt_name)
            prompt = dl.Prompt(key="prompt_from_annotations")
            prompt.add(mimetype=dl.PromptType.TEXT, value=text)
            prompt_item.add(prompt)
            output_item = item.dataset.items.upload(prompt_item, overwrite=True, remote_path=directory)
            logger.info(f"Created prompt item {output_item.id} from input item {item.id} at directory {directory} in "
                        f"dataset {item.dataset.name}")
            output_item.metadata["original_item"] = item.metadata.get("original_item", item.id)
            output_item = output_item.update()
            return output_item
        else:
            raise Exception(f"Item {item.id} has no text annotations")

    @staticmethod
    def create_prompt_from_annotation(annotation: dl.Annotation, context: dl.Context) -> dl.Item:
        node = context.node
        prompt_text = node.metadata['customNodeConfig']["prompt_text"]
        combine_texts = node.metadata['customNodeConfig']["combine_texts"]
        prefix = node.metadata['customNodeConfig']["prefix"]
        directory = node.metadata['customNodeConfig']["directory"]

        if prompt_text and combine_texts:
            text = prompt_text
        else:
            logger.warning("Failed to combine text item input with prompt. Using just annotation text input.")
            text = ''
        if annotation.type == dl.AnnotationType.TEXT:
            text += f" {annotation.coordinates}"
        elif annotation.type == dl.AnnotationType.SUBTITLE:
            text += f" {annotation.coordinates['text']}"
        else:
            raise TypeError(f"Annotation of type {annotation.type} is not supported by prompt tools.")
        prompt_name = f"{prefix}-{os.path.splitext(annotation.item.name)[0]}"
        prompt_item = dl.PromptItem(name=prompt_name)
        prompt = dl.Prompt(key="prompt_from_annotations")
        prompt.add(mimetype=dl.PromptType.TEXT, value=text)
        prompt_item.add(prompt)
        output_item = annotation.item.dataset.items.upload(prompt_item, overwrite=True, remote_path=directory)
        logger.info(f"Created prompt item {output_item.id} from input annotation {annotation.id} at directory {directory} in "
                    f"dataset {annotation.item.dataset.name}")
        output_item.metadata["original_item"] = annotation.item.metadata.get("original_item", annotation.item.id)
        output_item = output_item.update()
        return output_item
