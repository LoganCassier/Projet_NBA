from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
  "cerspense/zeroscope_v2_XL",  # modèle vidéo IA simple
  torch_dtype=torch.float16
).to("cuda")

video = pipe("Ironforge from WoW with Unreal Engine graphics, cinematic snow, fantasy").frames
