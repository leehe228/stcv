from __future__ import annotations

from ..schemas import PaperCandidate
from .text import keyword_overlap


OFFLINE_PAPERS: list[dict] = [
    {
        "title": "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances",
        "authors": ["Michael Ahn", "Anthony Brohan", "Noah Brown", "Yevgen Chebotar", "Omar Cortes"],
        "year": 2022,
        "venue": "arXiv",
        "url": "https://arxiv.org/abs/2204.01691",
        "source": "offline_seed",
        "abstract": "SayCan combines large language model planning with learned robotic affordances so that language plans are grounded in what a robot can execute.",
    },
    {
        "title": "PaLM-E: An Embodied Multimodal Language Model",
        "authors": ["Danny Driess", "Fei Xia", "Mehdi S. M. Sajjadi", "Corey Lynch", "Aakanksha Chowdhery"],
        "year": 2023,
        "venue": "ICML",
        "url": "https://arxiv.org/abs/2303.03378",
        "source": "offline_seed",
        "abstract": "PaLM-E injects continuous sensor observations into a language model to solve embodied reasoning, visual question answering, and robotic manipulation tasks.",
    },
    {
        "title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
        "authors": ["Anthony Brohan", "Noah Brown", "Justice Carbajal", "Yevgen Chebotar", "Xiaofeng Chen"],
        "year": 2023,
        "venue": "CoRL",
        "url": "https://arxiv.org/abs/2307.15818",
        "source": "offline_seed",
        "abstract": "RT-2 co-fine-tunes vision-language models on web data and robot trajectories to produce action tokens that transfer semantic knowledge to control.",
    },
    {
        "title": "Open X-Embodiment: Robotic Learning Datasets and RT-X Models",
        "authors": ["Open X-Embodiment Collaboration"],
        "year": 2023,
        "venue": "ICRA",
        "url": "https://arxiv.org/abs/2310.08864",
        "source": "offline_seed",
        "abstract": "Open X-Embodiment aggregates robot demonstrations from many embodiments and trains RT-X policies that improve cross-robot generalization.",
    },
    {
        "title": "VIMA: General Robot Manipulation with Multimodal Prompts",
        "authors": ["Yunfan Jiang", "Agrim Gupta", "Zichen Zhang", "Guanzhi Wang", "Yuke Zhu"],
        "year": 2022,
        "venue": "ICML",
        "url": "https://arxiv.org/abs/2210.03094",
        "source": "offline_seed",
        "abstract": "VIMA formulates robot manipulation as prompt-conditioned sequence modeling with multimodal prompts spanning text, images, and object references.",
    },
    {
        "title": "Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation",
        "authors": ["Mohan Shridhar", "Lucas Manuelli", "Dieter Fox"],
        "year": 2022,
        "venue": "CoRL",
        "url": "https://arxiv.org/abs/2209.05451",
        "source": "offline_seed",
        "abstract": "PerAct uses voxelized observations and a Perceiver transformer to learn language-conditioned manipulation policies across many tasks.",
    },
    {
        "title": "DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset",
        "authors": ["Alexander Khazatsky", "Karl Pertsch", "Suraj Nair", "Ashwin Balakrishna", "Sudeep Dasari"],
        "year": 2024,
        "venue": "RSS",
        "url": "https://arxiv.org/abs/2403.12945",
        "source": "offline_seed",
        "abstract": "DROID provides diverse in-the-wild robot demonstrations to study scalable imitation learning and robustness across environments.",
    },
    {
        "title": "Octo: An Open-Source Generalist Robot Policy",
        "authors": ["Octo Model Team", "Dibyendu Ghosh", "Homer Walke", "Karl Pertsch"],
        "year": 2024,
        "venue": "RSS Workshop",
        "url": "https://arxiv.org/abs/2405.12213",
        "source": "offline_seed",
        "abstract": "Octo trains a generalist robot policy on large mixed robot datasets with flexible goal specifications and open-source release.",
    },
    {
        "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
        "authors": ["Shunyu Yao", "Jeffrey Zhao", "Dian Yu", "Nan Du", "Izhak Shafran"],
        "year": 2023,
        "venue": "ICLR",
        "url": "https://arxiv.org/abs/2210.03629",
        "source": "offline_seed",
        "abstract": "ReAct interleaves reasoning traces with actions so language agents can use external tools and ground decisions in observations.",
    },
    {
        "title": "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
        "authors": ["Qingyun Wu", "Gagan Bansal", "Jieyu Zhang", "Yiran Wu", "Beibin Li"],
        "year": 2023,
        "venue": "arXiv",
        "url": "https://arxiv.org/abs/2308.08155",
        "source": "offline_seed",
        "abstract": "AutoGen presents a programming framework for composing multiple LLM agents that converse, call tools, and collaborate on complex tasks.",
    },
    {
        "title": "CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society",
        "authors": ["Guohao Li", "Hasan Abed Al Kader Hammoud", "Hani Itani", "Dmitrii Khizbullin", "Bernard Ghanem"],
        "year": 2023,
        "venue": "NeurIPS",
        "url": "https://arxiv.org/abs/2303.17760",
        "source": "offline_seed",
        "abstract": "CAMEL studies role-playing communicative agents and task decomposition through structured interactions among language-model agents.",
    },
    {
        "title": "Generative Agents: Interactive Simulacra of Human Behavior",
        "authors": ["Joon Sung Park", "Joseph C. O'Brien", "Carrie J. Cai", "Meredith Ringel Morris", "Percy Liang"],
        "year": 2023,
        "venue": "UIST",
        "url": "https://arxiv.org/abs/2304.03442",
        "source": "offline_seed",
        "abstract": "Generative Agents introduces memory, reflection, and planning modules that produce believable interactive behavior in simulated agents.",
    },
]


def search_offline(query: str, limit: int) -> list[PaperCandidate]:
    ranked = sorted(
        OFFLINE_PAPERS,
        key=lambda paper: keyword_overlap(query, paper["title"] + " " + paper["abstract"]),
        reverse=True,
    )
    return [PaperCandidate(**paper) for paper in ranked[:limit]]

