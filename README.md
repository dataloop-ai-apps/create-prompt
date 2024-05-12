# Prompt Tools

Create Dataloop prompt items from items or annotations. You can install it from the Dataloop Marketplace.

This app includes 3 pipeline nodes that can be used to create prompt items from a pipeline:

* **Create Prompt from Item**: Takes a media item (text, image or video) as input and generates a prompt item accordingly;
* **Create Prompt from Item Annotation**: Takes an item and generates a subsequent prompt item based on its annotations;
* **Create Prompt from Annotation**: Takes an annotation and creates a prompt item based on it;

For example, consider the following text item:
<img width="1507" alt="image" src="https://github.com/dataloop-ai-apps/prompt-tools/assets/124260926/2a98a367-166e-40f1-b3b9-432a1841e153">

could go through this pipeline:

<img width="883" alt="image" src="https://github.com/dataloop-ai-apps/prompt-tools/assets/124260926/036c93ea-b006-470f-8f21-8d729c41f068">

and create this prompt item, which could then be fed to LLM predictions:

<img width="975" alt="image" src="https://github.com/dataloop-ai-apps/prompt-tools/assets/124260926/2ba9fe26-1202-4ed9-adc7-84c8000c29f2">


### Configurations

The three nodes contain the same configurations:

<img width="333" alt="image" src="https://github.com/dataloop-ai-apps/prompt-tools/assets/124260926/458d434f-fb54-4f3a-a0f0-e1beb1d199d4">

* **Node Name**: The name that will be displayed in the node;
* **Prompt context**: The text typed in this field will be added to the beginning of the output prompt item, as a form of contextualizing. Can be left blank;
* **Combine texts**: Boolean option. If set to true, it will combine the prompt context to any text input in a single prompt. If set to false, the prompt context will be ignored. True by default;
* **Prefix**: The prompt item will be generated with the original file's name and this prefix added to it. The default is "prompt-"
* **Directory**: The prompt item will be saved in the original item's dataset, in the directory specified here. The default is "/.dataloop/prompts/" which is a hidden directory.

Additionally, the ```Create Prompt Item from Item Annotations``` contain this additional configuration option:

* **Annotation Type**: selection between the two types of annotation currently supported for prompt items: text and subtitle.
