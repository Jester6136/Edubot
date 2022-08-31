from custom_nlu.common import NotInstalled

try:
    from custom_nlu.tokenizer.VietnameseTokenizer import VietNamese_Tokenizer
except ImportError:
    ThaiTokenizer = NotInstalled("VietNamese_Tokenizer", "vi")


__all__ = ["VietNamese_Tokenizer"]
