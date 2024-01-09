from typing import Dict, List, Optional

from opencompass.models.base import BaseModel
from opencompass.utils import get_logger

try:
    from vllm import LLM, SamplingParams
except ImportError:
    LLM, SamplingParams = None, None

DEFAULT_MODEL_KWARGS = dict(trust_remote_code=True)


class VLLM(BaseModel):
    """Model Wrapper for VLLM."""

    def __init__(
        self,
        path: str,
        max_seq_len: int = 2048,
        model_kwargs: dict = None,
        generation_kwargs: dict = dict(),
        meta_template: Optional[Dict] = None,
        mode: str = 'none',
        use_fastchat_template: bool = False,
        end_str: Optional[str] = None,
    ):
        super().__init__(path=path,
                         max_seq_len=max_seq_len,
                         meta_template=meta_template)

        assert LLM, ('Please install VLLM with `pip install vllm`. '
                     'note: torch==2.1.2 is required.')
        self.logger = get_logger()
        self._load_model(path, model_kwargs)
        self.tokenizer = self.model.get_tokenizer()
        self.generation_kwargs = generation_kwargs
        self.generation_kwargs.pop('do_sample', None)

        assert mode in ['none', 'mid']
        self.mode = mode
        self.use_fastchat_template = use_fastchat_template
        self.end_str = end_str

    def _load_model(self,
                    path: str,
                    add_model_kwargs: dict = None,
                    num_retry: int = 3):
        model_kwargs = DEFAULT_MODEL_KWARGS.copy()
        if add_model_kwargs is not None:
            model_kwargs.update(add_model_kwargs)
        self.model = LLM(path, **model_kwargs)

    def generate(self, inputs: List[str], max_out_len: int,
                 **kwargs) -> List[str]:
        """Generate results given a list of inputs.

        Args:
            inputs (List[str]): A list of strings.
            max_out_len (int): The maximum length of the output.

        Returns:
            List[str]: A list of generated strings.
        """

        if self.mode == 'mid':
            input_ids = self.tokenizer(inputs, truncation=False)['input_ids']
            inputs = []
            for input_id in input_ids:
                if len(input_id) > self.max_seq_len - max_out_len:
                    half = int((self.max_seq_len - max_out_len) / 2)
                    inputs.append(
                        self.tokenizer.decode(input_id[:half],
                                              skip_special_tokens=True) +
                        self.tokenizer.decode(input_id[-half:],
                                              skip_special_tokens=True))
                else:
                    inputs.append(
                        self.tokenizer.decode(input_id,
                                              skip_special_tokens=True))

        generation_kwargs = kwargs.copy()
        generation_kwargs.update(self.generation_kwargs)
        generation_kwargs.update({'max_tokens': max_out_len})
        sampling_kwargs = SamplingParams(**generation_kwargs)
        outputs = self.model.generate(inputs, sampling_kwargs)

        prompt_list, output_strs = [], []
        for output in outputs:
            prompt = output.prompt
            generated_text = output.outputs[0].text

            if self.end_str:
                generated_text = generated_text.split(self.end_str)[0]
            prompt_list.append(prompt)
            output_strs.append(generated_text)

        return output_strs

    def prompts_preproccess(self, inputs: List[str]):
        if self.use_fastchat_template:
            try:
                from fastchat.model import get_conversation_template
            except ModuleNotFoundError:
                raise ModuleNotFoundError(
                    'Fastchat is not implemented. You can use '
                    "'pip install \"fschat[model_worker,webui]\"' "
                    'to implement fastchat.')
            conv = get_conversation_template('vicuna')
            conv.append_message(conv.roles[0], inputs[0])
            conv.append_message(conv.roles[1], None)
            inputs = [conv.get_prompt()]
        return inputs

    def get_token_len(self, prompt: str) -> int:
        """Get lengths of the tokenized strings.

        Args:
            prompt (str): Input string.

        Returns:
            int: Length of the input tokens
        """
        return len(self.model.get_tokenizer().encode(prompt))
