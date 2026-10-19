# Third-Party Notices - Reels Sin Editor 1.3.0

*Reels Sin Editor usa los componentes de terceros que se listan abajo. Sus licencias y autores se indican aqui; cada componente sigue bajo su propia licencia.*

Reels Sin Editor ("the Product") uses the third-party components listed below. Each remains the property of its authors and is licensed under its own terms, which are not changed by the Product's licence agreement. "Delivered" means included in or hosted by the Product; "Downloaded" means your installer fetches it from the original source onto your computer when you run setup (it is not part of the Product package).

Notices verified 2026-10-19.

## 1. Speech and audio models

| Component | Used for | Author / owner | Licence | How supplied | URL |
|---|---|---|---|---|---|
| Audio classifier (panns_speech.onnx) | Detects breath, chair and noise stretches so they can be cut | Kong, Cao, Iqbal, Wang, Wang, Plumbley (PANNs) | CC BY 4.0 | Hosted by Reels Sin Editor, downloaded at setup | https://zenodo.org/records/3987831 |
| NVIDIA Parakeet TDT 0.6B v3 (ONNX conversion by istupakov for onnx-asr) | Speech to text with word timing | NVIDIA; ONNX conversion by istupakov | CC BY 4.0 | Downloaded from Hugging Face | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 , https://huggingface.co/istupakov/parakeet-tdt-0.6b-v3-onnx |
| faster-whisper large-v3 (CTranslate2 conversion of OpenAI Whisper large-v3) | Speech to text (fallback and Whisper mode) | Systran (conversion); OpenAI (original Whisper) | MIT | Downloaded from Hugging Face | https://huggingface.co/Systran/faster-whisper-large-v3 |
| Silero VAD | Detects where speech is | Silero Team | MIT, Copyright (c) 2020-present Silero Team | Downloaded (Python package) | https://github.com/snakers4/silero-vad |
| MODNet portrait matting (ONNX by Xenova) | Separates the person from the background | Zhanghan Ke et al. (MODNet); ONNX export by Xenova | Apache License 2.0 | Downloaded from Hugging Face | https://github.com/ZHKKKe/MODNet , https://huggingface.co/Xenova/modnet |

Required statement for the audio classifier:

> Audio classifier based on PANNs (Kong et al., 2020), licensed CC BY 4.0, converted to ONNX and reduced to the speech output by Reels Sin Editor. Source: https://zenodo.org/records/3987831 . Licence: https://creativecommons.org/licenses/by/4.0/ . Original authors do not endorse Reels Sin Editor.

Reference: Q. Kong, Y. Cao, T. Iqbal, Y. Wang, W. Wang, M. D. Plumbley, "PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition", IEEE/ACM Transactions on Audio, Speech, and Language Processing 28 (2020): 2880-2894. DOI of the checkpoint record: 10.5281/zenodo.3987831.

Parakeet (CC BY 4.0): "NVIDIA Parakeet TDT 0.6B v3" by NVIDIA, licensed CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . It is used unmodified by the Product; the ONNX conversion is by istupakov.

faster-whisper large-v3: the model files are a float16 CTranslate2 conversion of openai/whisper-large-v3 published by Systran under MIT. The MIT licence of the model repository and of faster-whisper applies; copyright notices are in those repositories.

## 2. Video and rendering tools (downloaded into a private folder on your computer)

| Component | Used for | Author / owner | Licence | URL |
|---|---|---|---|---|
| FFmpeg (conda-forge build 9.0.2, GPL variant with x264 and x265) | Cutting, encoding and mixing video and audio | FFmpeg developers; x264 (VideoLAN), x265 (MulticoreWare) | GPL-2.0-or-later (as declared by the package) | https://ffmpeg.org , https://github.com/conda-forge/ffmpeg-feedstock |
| Python 3.12 (conda-forge) | Runs the Product's engine | Python Software Foundation | Python-2.0 (PSF) | https://www.python.org/psf/license/ |
| Node.js (conda-forge) | Runs the animation and render tools | OpenJS Foundation and contributors | MIT | https://github.com/nodejs/node |
| micromamba 2.9.0 | Creates the private environment | QuantStack and the Mamba contributors | BSD-3-Clause, Copyright 2019 QuantStack and the Mamba contributors | https://github.com/mamba-org/mamba |
| conda-forge packages (lame, libass, openh264 and others pulled in with FFmpeg) | Audio/video codecs and subtitle rendering used by FFmpeg | Respective authors | Per package: LGPL-2.0-only (lame), ISC (libass), BSD-2-Clause (openh264) | https://conda-forge.org |
| HyperFrames 0.8.140 (run with npx) | Renders the finished video from HTML | HeyGen, Inc. | Apache License 2.0, Copyright 2026 HeyGen, Inc. | https://github.com/heygen-com/hyperframes |
| Chrome headless shell (Chrome for Testing) | Headless browser used by the renderer | Google LLC and Chromium contributors | NOT VERIFIED (Chromium open-source licences plus Google terms; see VERIFICATION.md) | https://github.com/GoogleChromeLabs/chrome-for-testing |
| capcut-cli 0.28.0 | Writes editable CapCut projects | Rene Zander | MIT | https://github.com/renezander030/capcut-cli |

FFmpeg: the FFmpeg build is downloaded and run as a separate program; the Product does not include it. The source code of FFmpeg, x264 and x265 is available from the project pages above and from conda-forge (https://github.com/conda-forge/ffmpeg-feedstock). You may replace this FFmpeg with your own build.

HyperFrames installs further npm packages (for example hono, puppeteer-core, sharp, esbuild, prettier) under their own licences, which npm records inside each package folder on your computer.

## 3. Python libraries (downloaded with pip into the private environment)

| Library | Used for | Author / owner | Licence | URL |
|---|---|---|---|---|
| faster-whisper 1.2.1 | Whisper speech recognition | SYSTRAN | MIT | https://github.com/SYSTRAN/faster-whisper |
| CTranslate2 4.8.2 | Fast model engine | OpenNMT / SYSTRAN | MIT | https://opennmt.net |
| ONNX Runtime 1.30.0 | Runs ONNX models | Microsoft | MIT | https://onnxruntime.ai |
| onnx-asr | Runs Parakeet | Ilya Stupakov | MIT | https://github.com/istupakov/onnx-asr |
| silero-vad | Voice activity detection | Silero Team | MIT | https://github.com/snakers4/silero-vad |
| PyAV 19.0.1 | Reading video and audio | PyAV contributors | BSD-3-Clause (the wheel bundles FFmpeg libraries, see section 2 note) | https://github.com/PyAV-Org/PyAV |
| NumPy 2.5.3 | Numerics | NumPy Developers | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | https://numpy.org |
| SciPy | Signal processing | SciPy Developers | BSD-3-Clause (bundled OpenBLAS/LAPACK BSD; GCC runtime libraries under GPL-3.0 with GCC exception and LGPL-2.1) | https://scipy.org |
| soundfile | Reading audio | Bastian Bechtold | BSD-3-Clause (wheel bundles libsndfile, LGPL) | https://github.com/bastibe/python-soundfile |
| PyTorch (CPU, pulled in by silero-vad) | Loader for Silero | PyTorch contributors | Declared as Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT (PyPI) | https://pytorch.org |
| OpenCV (opencv-python-headless 4.14.0.94) | Face tracking and image work | OpenCV team | Apache-2.0 (bundles FFmpeg under LGPL; see its LICENSE-3RD-PARTY.txt) | https://github.com/opencv/opencv-python |
| Pillow 12.3.0 | Images | Jeffrey A. Clark and contributors | MIT-CMU | https://python-pillow.org |
| huggingface_hub 1.33.0 | Downloads models | Hugging Face | Apache-2.0 | https://github.com/huggingface/huggingface_hub |
| fontTools 4.67.0 | Reads font files | Just van Rossum and contributors | MIT | https://github.com/fonttools/fonttools |
| tqdm | Progress bars | tqdm developers | MPL-2.0 AND MIT | https://github.com/tqdm/tqdm |
| yt-dlp | Optional: downloads a reference video you give it. You are responsible for having the right to download and use that material and for the terms of the site it comes from (Licence, section 6) | yt-dlp contributors | Unlicense (public domain) | https://github.com/yt-dlp/yt-dlp |
| Their dependencies (anyio, certifi, click, filelock, flatbuffers, fsspec, h11, hf-xet, httpcore, httpx, idna, packaging, protobuf, PyYAML, tokenizers, typing_extensions) | Support libraries | Respective authors | MIT, BSD, Apache-2.0, PSF-2.0; certifi is MPL-2.0 | listed on PyPI |

## 4. JavaScript libraries (downloaded with npm)

| Library | Used for | Author / owner | Licence | URL |
|---|---|---|---|---|
| GSAP 3.15.0 | Animation of captions and graphics inside the render | GreenSock / Webflow, Inc. | GSAP Standard "no charge" License (effective 30 Apr 2025) | https://gsap.com/community/standard-license/ |

GSAP: used under the GSAP Standard License, which does not require attribution but forbids removing GSAP's notices. The Product does not include GSAP; it is downloaded from npm to your computer.

## 5. Fonts (delivered inside the Product, folder fonts/ and fonts/pack/)

All 18 fonts are licensed under the SIL Open Font License 1.1 (https://openfontlicense.org). The licence text is in fonts/pack/OFL.txt and the copyright notices are in fonts/pack/NOTICES.txt. The fonts may be used in your videos at no charge; they may not be sold on their own.

| Font | Copyright |
|---|---|
| Anton | Copyright 2020 The Anton Project Authors |
| Bebas Neue | Copyright 2010 by Dharma Type |
| Oswald | Copyright 2016 The Oswald Project Authors |
| Barlow Condensed (Bold, ExtraBold) | Copyright 2017 The Barlow Project Authors |
| Montserrat (regular, italic) | Copyright 2011 The Montserrat Project Authors |
| Plus Jakarta Sans | Copyright 2020 The Plus Jakarta Sans Project Authors |
| Nunito Sans | Copyright 2016 The Nunito Sans Project Authors |
| Bodoni Moda Italic | Copyright 2020 The Bodoni Moda Project Authors |
| EB Garamond Italic | Copyright 2017 The EB Garamond Project Authors |
| Libre Baskerville Italic | Copyright (c) 2012 Pablo Impallari, Rodrigo Fuenzalida, Reserved Font Name Libre Baskerville |
| Spectral Italic | Copyright 2017 The Spectral Project Authors |
| Crimson Italic | Copyright (c) 2010 Sebastian Kosch, Reserved Font Name Crimson |
| Cinzel Decorative Bold | Copyright (c) 2012 Natanael Gama, Reserved Font Name Cinzel |
| Playfair Display Italic | Copyright 2017 The Playfair Display Project Authors, Reserved Font Name Playfair Display |
| Inter | Copyright 2016 The Inter Project Authors |
| Indie Flower | Copyright 2010 The Indie Flower Authors |

## 6. Other

| Item | Note |
|---|---|
| Sound effects and music beds (sounds/) | Synthesised by the Reels Sin Editor authors; no third-party recordings or samples. |
| Effects library, icons (effects/, effects/studio/icons.json) | Created by the Reels Sin Editor authors. |

Disclaimer: all third-party components are provided by their authors "as is" without warranty. Names of third parties are used only to identify them and do not imply endorsement.

---
*(c) 2026 melimoyano.com. Todos los derechos reservados. Reels Sin Editor se licencia, no se vende: queda prohibido copiar, reproducir, compartir, recrear, imitar, revender o crear obras derivadas de este material, en todo o en parte, y usarlo para entrenar IA. Ver el archivo LICENSE.*

*(c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.*
