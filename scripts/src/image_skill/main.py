#!/usr/bin/env python3
"""
Modelscope Image Generation CLI
Usage:
    python main.py generate "A golden cat" --model Tongyi-MAI/Z-Image-Turbo
    python main.py edit ./cat.jpg "Make the cat wear a hat"
    python main.py generate "A golden cat" --no-wait   # returns a task id right away
    python main.py status <task_id> --wait             # block on it later, elsewhere
    python main.py list-models
    python main.py set-model Qwen/Qwen-Image
    python main.py current-model
"""

import argparse
import sys
from pathlib import Path

from image_skill.modelscope_client import ModelscopeClient, ConfigManager, default_config_path


def cmd_generate(args):
    client = ModelscopeClient(config_path=args.config)

    if args.model:
        if not client.set_model(args.model):
            print(f"Error: Model '{args.model}' not found in config")
            sys.exit(1)

    print(f"Using model: {client.get_current_model()}")
    print(f"Prompt: {args.prompt}")

    try:
        if args.no_wait:
            task_id = client.submit_generate(
                prompt=args.prompt,
                negative_prompt=args.negative_prompt,
                steps=args.steps,
                cfg_scale=args.cfg_scale,
                width=args.width,
                height=args.height,
                seed=args.seed,
            )
            print(f"\nTask submitted: {task_id}")
            print(f"Check status with: image-gen status {task_id}")
            return

        paths = client.generate_and_save(
            prompt=args.prompt,
            output_dir=args.output,
            prefix=args.prefix,
            negative_prompt=args.negative_prompt,
            steps=args.steps,
            cfg_scale=args.cfg_scale,
            width=args.width,
            height=args.height,
            seed=args.seed,
        )
        print(f"\nGenerated {len(paths)} image(s):")
        for p in paths:
            print(f"  {p}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


EDIT_DEFAULT_MODEL = "Qwen/Qwen-Image-Edit"


def cmd_edit(args):
    client = ModelscopeClient(config_path=args.config)
    model = args.model or EDIT_DEFAULT_MODEL

    print(f"Using model: {model}")
    print(f"Source image: {args.image}")
    print(f"Prompt: {args.prompt}")

    try:
        if args.no_wait:
            task_id = client.submit_edit(
                image=args.image,
                prompt=args.prompt,
                model=model,
                negative_prompt=args.negative_prompt,
                steps=args.steps,
                cfg_scale=args.cfg_scale,
                width=args.width,
                height=args.height,
                seed=args.seed,
            )
            print(f"\nTask submitted: {task_id}")
            print(f"Check status with: image-gen status {task_id}")
            return

        paths = client.edit_and_save(
            image=args.image,
            prompt=args.prompt,
            model=model,
            output_dir=args.output,
            prefix=args.prefix,
            negative_prompt=args.negative_prompt,
            steps=args.steps,
            cfg_scale=args.cfg_scale,
            width=args.width,
            height=args.height,
            seed=args.seed,
        )
        print(f"\nEdited {len(paths)} image(s):")
        for p in paths:
            print(f"  {p}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_status(args):
    client = ModelscopeClient(config_path=args.config)

    try:
        if args.wait:
            urls = client.wait_for_task(args.task_id)
        else:
            data = client.get_task_status(args.task_id)
            status = data.get("task_status")
            print(f"Status: {status}")

            if status == "FAILED":
                error = data.get("error", "Unknown error")
                print(f"Error: {error}")
                sys.exit(1)
            elif status != "SUCCEED":
                return  # still running — nothing more to report yet

            urls = data.get("output_images", [])

        paths = client.save_urls(urls, args.output, args.prefix)
        print(f"\nSaved {len(paths)} image(s):")
        for p in paths:
            print(f"  {p}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_list_models(args):
    config_manager = ConfigManager(args.config)
    models = config_manager.list_models()

    print("Available models:")
    for m in models:
        lora_str = " (LoRA supported)" if m.supports_lora else ""
        print(f"  {m.id}")
        print(f"    Name: {m.name}")
        print(f"    Description: {m.description}{lora_str}")
        print()


def cmd_set_model(args):
    config_manager = ConfigManager(args.config)
    model = config_manager.get_model(args.model_id)

    if not model:
        print(f"Error: Model '{args.model_id}' not found in config")
        sys.exit(1)

    config_path = Path(args.config)
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    data["modelscope"]["default_model"] = args.model_id

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print(f"Default model set to: {args.model_id}")


def cmd_current_model(args):
    config_manager = ConfigManager(args.config)
    print(f"Current default model: {config_manager.config.default_model}")


import yaml


def main():
    parser = argparse.ArgumentParser(description="Modelscope Image Generation CLI")
    parser.add_argument("-c", "--config", default=default_config_path(), help="Config file path")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate command
    gen_parser = subparsers.add_parser("generate", aliases=["g"], help="Generate image")
    gen_parser.add_argument("prompt", help="Prompt for image generation")
    gen_parser.add_argument("-m", "--model", help="Model ID to use")
    gen_parser.add_argument("-o", "--output", help="Output directory")
    gen_parser.add_argument("-p", "--prefix", default="generated", help="Output filename prefix")
    gen_parser.add_argument("--negative-prompt", help="Negative prompt")
    gen_parser.add_argument("--steps", type=int, help="Number of inference steps")
    gen_parser.add_argument("--cfg-scale", type=float, help="CFG scale")
    gen_parser.add_argument("--width", type=int, help="Image width")
    gen_parser.add_argument("--height", type=int, help="Image height")
    gen_parser.add_argument("--seed", type=int, help="Random seed")
    gen_parser.add_argument(
        "--no-wait", action="store_true",
        help="Submit and return immediately with a task id instead of blocking until done; check later with `image-gen status`",
    )

    # edit command
    edit_parser = subparsers.add_parser("edit", aliases=["e"], help="Edit an existing image")
    edit_parser.add_argument("image", help="Path or URL of the source image to edit")
    edit_parser.add_argument("prompt", help="Prompt describing the edit")
    edit_parser.add_argument("-m", "--model", help=f"Model ID to use (default: {EDIT_DEFAULT_MODEL})")
    edit_parser.add_argument("-o", "--output", help="Output directory")
    edit_parser.add_argument("-p", "--prefix", default="edited", help="Output filename prefix")
    edit_parser.add_argument("--negative-prompt", help="Negative prompt")
    edit_parser.add_argument("--steps", type=int, help="Number of inference steps")
    edit_parser.add_argument("--cfg-scale", type=float, help="CFG scale")
    edit_parser.add_argument("--width", type=int, help="Output width")
    edit_parser.add_argument("--height", type=int, help="Output height")
    edit_parser.add_argument("--seed", type=int, help="Random seed")
    edit_parser.add_argument(
        "--no-wait", action="store_true",
        help="Submit and return immediately with a task id instead of blocking until done; check later with `image-gen status`",
    )

    # status command
    status_parser = subparsers.add_parser("status", aliases=["st"], help="Check or wait on a task submitted with --no-wait")
    status_parser.add_argument("task_id", help="Task id printed by a --no-wait generate/edit call")
    status_parser.add_argument("--wait", action="store_true", help="Block until the task completes instead of checking once")
    status_parser.add_argument("-o", "--output", help="Output directory")
    status_parser.add_argument("-p", "--prefix", default="generated", help="Output filename prefix")

    # list-models command
    subparsers.add_parser("list-models", aliases=["ls"], help="List available models")

    # set-model command
    set_parser = subparsers.add_parser("set-model", aliases=["sm"], help="Set default model")
    set_parser.add_argument("model_id", help="Model ID to set as default")

    # current-model command
    subparsers.add_parser("current-model", aliases=["cm"], help="Show current default model")

    args = parser.parse_args()

    commands = {
        "generate": cmd_generate,
        "g": cmd_generate,
        "edit": cmd_edit,
        "e": cmd_edit,
        "status": cmd_status,
        "st": cmd_status,
        "list-models": cmd_list_models,
        "ls": cmd_list_models,
        "set-model": cmd_set_model,
        "sm": cmd_set_model,
        "current-model": cmd_current_model,
        "cm": cmd_current_model,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()