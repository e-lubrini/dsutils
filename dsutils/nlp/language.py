
import imp
import nltk
from nltk.tokenize import sent_tokenize
from dsutils.de.files import *
#from dsutils.de.utils import *

nltk.download('words')

from deep_translator import GoogleTranslator
from tqdm import tqdm
import fasttext

def get_lang_code(lang_name):
    import langcodes as lc
    #lang_name = str(lang_name)
    if type(lang_name) is str and len(lang_name) > 0:
        lang_code = lc.find(lang_name)
    else:
        lang_code = lang_name
    return str(lang_code)

def translate_to_lang(txt,
                source_lang_code,
                targ_lang_code,
                ):
    sents = sent_tokenize(txt)
    trans_sents = list()
    for sent in tqdm(sents, desc='translated sentences', leave=False):
        try:
            trans_sent = str((GoogleTranslator(source_lang_code,targ_lang_code).translate(str(sent))))
        except:
            trans_sent = str(sent)
        trans_sents.append(trans_sent)
    translation = ' '.join(trans_sents)
    return translation

# get translation if needed
def get_translation(tool_dir_path,
                    source_text,
                    source_lang_code,
                    targ_lang_code,
                    storage_opts=True,
                    overwrite_opts=True,
                    ):
    src_type = get_var_name(source_text)
    translation = try_read(os.path.join(tool_dir_path, 'translation.txt'))
    needs_trans = storage_opts[src_type+'_trans'] and (overwrite_opts[src_type+'_trans'] or not translation)
    if needs_trans:
        translation = translate_to_lang(source_text,
                                        source_lang_code=source_lang_code,
                                        targ_lang_code=targ_lang_code,
                                        )
    return translation


def get_langs(prep_text,     # text whose language is to be detected
            lang_n=1    # how many possible lang_codes we want to detect (in order from most to least probable)
            ):
    model = fasttext.load_model(os.path.join('models','lid.176.ftz'))
    prediction = (model.predict(prep_text, k=lang_n))[0] # tuple of language codes and respective probabilities
    lang_codes = [label[-2:] for label in prediction]
    return lang_codes    # list of language code(s) detected