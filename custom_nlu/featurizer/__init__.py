from custom_nlu.common import NotInstalled

try:
    from custom_nlu.featurizer.FastTextFeaturizer import FastTextFeaturizer
except ImportError:
    FastTextFeaturizer = NotInstalled("fasttext", "fasttext")

__all__ = ["FastTextFeaturizer"]
