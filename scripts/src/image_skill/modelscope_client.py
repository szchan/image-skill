import os
import json
import time
import base64
import mimetypes
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from io import BytesIO

import requests
import yaml
from PIL import Image


@dataclass
class ModelConfig:
    id: str
    name: str
    description: str
    supports_lora: bool = False


@dataclass
class GenerationConfig:
    default_prompt: str = "A golden cat"
    default_negative_prompt: str = ""
    default_steps: int = 20
    default_cfg_scale: float = 7.0
    default_width: int = 1024
    default_height: int = 1024
    output_dir: str = "./outputs"
    poll_interval: int = 5
    timeout: int = 300


@dataclass
class ModelScopeConfig:
    api_key: str
    base_url: str = "https://api-inference.modelscope.cn/"
    default_model: str = "Tongyi-MAI/Z-Image-Turbo"
    async_mode: bool = True
    models: List[ModelConfig] = field(default_factory=list)
    generation: GenerationConfig = field(default_factory=GenerationConfig)


class ConfigManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self._config: Optional[ModelScopeConfig] = None

    def load(self) -> ModelScopeConfig:
        if self._config is not None:
            return self._config

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        ms_data = data.get("modelscope", {})
        models_data = data.get("models", [])
        gen_data = data.get("generation", {})

        models = [ModelConfig(**m) for m in models_data]
        generation = GenerationConfig(**gen_data)

        self._config = ModelScopeConfig(
            api_key=ms_data.get("api_key", ""),
            base_url=ms_data.get("base_url", "https://api-inference.modelscope.cn/"),
            default_model=ms_data.get("default_model", "Tongyi-MAI/Z-Image-Turbo"),
            async_mode=ms_data.get("async_mode", True),
            models=models,
            generation=generation,
        )
        return self._config

    def get_model(self, model_id: str) -> Optional[ModelConfig]:
        config = self.load()
        for m in config.models:
            if m.id == model_id:
                return m
        return None

    def list_models(self) -> List[ModelConfig]:
        return self.load().models

    @property
    def config(self) -> ModelScopeConfig:
        if self._config is None:
            self.load()
        return self._config


class ModelscopeClient:
    def __init__(self, config: Optional[ModelScopeConfig] = None, config_path: str = "config.yaml"):
        self.config_manager = ConfigManager(config_path)
        self.config = config or self.config_manager.load()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        })

    def set_model(self, model_id: str) -> bool:
        model = self.config_manager.get_model(model_id)
        if model:
            self.config.default_model = model_id
            return True
        return False

    def get_current_model(self) -> str:
        return self.config.default_model

    def list_available_models(self) -> List[ModelConfig]:
        return self.config_manager.list_models()

    @staticmethod
    def _build_generate_payload(
        prompt: str,
        model_id: str,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model_id,
            "prompt": prompt,
        }

        if loras:
            payload["loras"] = loras
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if steps:
            payload["steps"] = steps
        if cfg_scale:
            payload["cfg_scale"] = cfg_scale
        if width:
            payload["width"] = width
        if height:
            payload["height"] = height
        if seed is not None:
            payload["seed"] = seed

        return payload

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> List[str]:
        payload = self._build_generate_payload(
            prompt, model or self.config.default_model, loras, negative_prompt,
            steps, cfg_scale, width, height, seed,
        )
        return self._submit(payload)

    def submit_generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> str:
        """Submit a generate job and return its task_id immediately, without
        waiting for completion. Poll it later with get_task_status() or
        block on it with wait_for_task(). Requires async_mode: true."""
        payload = self._build_generate_payload(
            prompt, model or self.config.default_model, loras, negative_prompt,
            steps, cfg_scale, width, height, seed,
        )
        return self._submit_only(payload)

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = dict(self.session.headers)
        if self.config.async_mode:
            headers["X-ModelScope-Async-Mode"] = "true"

        response = self.session.post(
            f"{self.config.base_url}v1/images/generations",
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        )
        response.raise_for_status()
        return response.json()

    def _submit(self, payload: Dict[str, Any]) -> List[str]:
        result = self._post(payload)
        if self.config.async_mode:
            return self._wait_for_completion(result["task_id"])
        return result.get("output_images", [])

    def _submit_only(self, payload: Dict[str, Any]) -> str:
        if not self.config.async_mode:
            raise RuntimeError(
                "Submitting without waiting requires modelscope.async_mode: true in config.yaml "
                "(sync mode has no task_id to check later)"
            )
        return self._post(payload)["task_id"]

    @staticmethod
    def _encode_image(image: str) -> Dict[str, str]:
        """Build the payload field for an input image: a remote URL is passed
        through as `image_url`; a local path is base64-encoded into `image`
        as a data URI, since the API accepts either."""
        if image.startswith("http://") or image.startswith("https://"):
            return {"image_url": image}

        path = Path(image)
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return {"image": f"data:{mime};base64,{data}"}

    def _build_edit_payload(
        self,
        image: str,
        prompt: str,
        model_id: str,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model_id,
            "prompt": prompt,
            **self._encode_image(image),
        }

        if loras:
            payload["loras"] = loras
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if steps:
            payload["steps"] = steps
        if cfg_scale:
            payload["cfg_scale"] = cfg_scale
        if width:
            payload["width"] = width
        if height:
            payload["height"] = height
        if seed is not None:
            payload["seed"] = seed

        return payload

    def edit(
        self,
        image: str,
        prompt: str,
        model: Optional[str] = None,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> List[str]:
        """Edit an existing image with a prompt. `image` is a local file path
        or a remote URL. Use an editing-capable model such as
        Qwen/Qwen-Image-Edit."""
        payload = self._build_edit_payload(
            image, prompt, model or self.config.default_model, loras,
            negative_prompt, steps, cfg_scale, width, height, seed,
        )
        return self._submit(payload)

    def submit_edit(
        self,
        image: str,
        prompt: str,
        model: Optional[str] = None,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> str:
        """Submit an edit job and return its task_id immediately, without
        waiting for completion. Poll it later with get_task_status() or
        block on it with wait_for_task(). Requires async_mode: true."""
        payload = self._build_edit_payload(
            image, prompt, model or self.config.default_model, loras,
            negative_prompt, steps, cfg_scale, width, height, seed,
        )
        return self._submit_only(payload)

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """One non-blocking check of a submitted task. Returns the raw
        Modelscope task JSON — inspect `task_status` (`SUCCEED`/`FAILED`/
        still-running) and, once succeeded, `output_images`."""
        headers = dict(self.session.headers)
        headers["X-ModelScope-Task-Type"] = "image_generation"

        response = self.session.get(
            f"{self.config.base_url}v1/tasks/{task_id}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def wait_for_task(self, task_id: str) -> List[str]:
        """Block, polling at `generation.poll_interval`, until the task
        succeeds (returning its output image URLs), fails (raising), or
        exceeds `generation.timeout` (raising TimeoutError)."""
        return self._wait_for_completion(task_id)

    def _wait_for_completion(self, task_id: str) -> List[str]:
        start_time = time.time()

        while True:
            if time.time() - start_time > self.config.generation.timeout:
                raise TimeoutError(f"Task {task_id} timed out after {self.config.generation.timeout}s")

            data = self.get_task_status(task_id)

            status = data.get("task_status")
            if status == "SUCCEED":
                return data.get("output_images", [])
            elif status == "FAILED":
                error = data.get("error", "Unknown error")
                raise RuntimeError(f"Image generation failed: {error}")

            time.sleep(self.config.generation.poll_interval)

    def download_and_save(self, image_url: str, output_path: Path) -> Path:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.save(output_path)
        return output_path

    def save_urls(self, urls: List[str], output_dir: Optional[str] = None, prefix: str = "generated") -> List[Path]:
        output_dir = Path(output_dir or self.config.generation.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_paths = []
        for i, url in enumerate(urls):
            timestamp = int(time.time())
            filename = f"{prefix}_{timestamp}_{i}.jpg"
            output_path = output_dir / filename
            saved = self.download_and_save(url, output_path)
            saved_paths.append(saved)

        return saved_paths

    def generate_and_save(
        self,
        prompt: str,
        output_dir: Optional[str] = None,
        prefix: str = "generated",
        **kwargs,
    ) -> List[Path]:
        urls = self.generate(prompt, **kwargs)
        return self.save_urls(urls, output_dir, prefix)

    def edit_and_save(
        self,
        image: str,
        prompt: str,
        output_dir: Optional[str] = None,
        prefix: str = "edited",
        **kwargs,
    ) -> List[Path]:
        urls = self.edit(image, prompt, **kwargs)
        return self.save_urls(urls, output_dir, prefix)


async def async_generate(
    client: ModelscopeClient,
    prompt: str,
    **kwargs,
) -> List[str]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: client.generate(prompt, **kwargs))