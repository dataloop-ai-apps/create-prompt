import dtlpy as dl
import os
import logging

logger = logging.getLogger(name="[CreatePrompt]")


class ServiceRunner(dl.BaseServiceRunner):

    def create_image_prompt(self, item: dl.Item, dataset: dl.Dataset, directory: str) -> dl.Item:
        if 'image' in item.mimetype:
            image_name = os.path.splitext(item.name)[0]
            prompt_item = dl.PromptItem(name=f"image_prompt_{image_name}")
            prompt = dl.Prompt(key="image")
            prompt.add(mimetype=dl.PromptType.IMAGE, value=item.stream)
            prompt_item.add(prompt)
            image_prompt_item = dataset.items.upload(prompt_item, overwrite=True, remote_path=directory)
            logger.info(f"Created prompt item {image_prompt_item.id} from image item {item.id} at"
                        f"directory {directory} in dataset {dataset.name}")
            return image_prompt_item
        else:
            raise TypeError(f"Item {item.id} is not an image")
