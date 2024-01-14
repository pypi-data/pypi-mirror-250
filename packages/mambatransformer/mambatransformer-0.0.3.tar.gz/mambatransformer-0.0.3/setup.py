# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mamba_transformer']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'mambatransformer',
    'version': '0.0.3',
    'description': 'MambaTransformer - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Mamba Transformer\n\n![Mamba Transformer](/mm_transformer.png)\n\nIntegrating Mamba/SSMs with Transformer for Enhanced Long Context and High-Quality Sequence Modeling.\n\nThis is 100% novel architecture that I have designed to combine the strengths and weaknesses out of SSMs and Attention for an all-new advanced architecture with the purpose of surpassing our old limits. Faster processing speed, longer context lengths, lower perplexity over long sequences, enhanced and superior reasoning while remaining small and compact.\n\nThe architecture is essentially: `x -> norm -> mamba -> norm -> transformer -> norm -> ffn -> norm -> out`.\n\nI added in many normalizations as I believe by default training stability would be severly degraded due to 2 foreign architecture's integrating with one another.\n\n\n## Install\n`pip3 install mambatransformer`\n\n\n### Usage\n```python\nimport torch\nfrom mamba_transformer import MambaTransformer\n\n# Generate a random tensor of shape (1, 10) with values between 0 and 99\nx = torch.randint(0, 100, (1, 10))\n\n# Create an instance of the MambaTransformer model\nmodel = MambaTransformer(\n    num_tokens=100,  # Number of tokens in the input sequence\n    dim=512,  # Dimension of the model\n    heads=8,  # Number of attention heads\n    depth=4,  # Number of transformer layers\n    dim_head=64,  # Dimension of each attention head\n    d_state=512,  # Dimension of the state\n    dropout=0.1,  # Dropout rate\n    ff_mult=4,  # Multiplier for the feed-forward layer dimension\n    return_embeddings=False,  # Whether to return the embeddings,\n    transformer_depth=2,  # Number of transformer blocks\n    mamba_depth=10,  # Number of Mamba blocks\n)\n\n# Pass the input tensor through the model and print the output shape\nprint(model(x).shape)\n\n\n# to train\nmodel.eval()\n\n# Would you like to train this model? Zeta Corporation offers unmatchable GPU clusters at unbeatable prices, let's partner!\n\n# Tokenizer\nmodel.generate(text)\n\n\n```\n\n# License\nMIT\n\n\n\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/MambaTransformer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
