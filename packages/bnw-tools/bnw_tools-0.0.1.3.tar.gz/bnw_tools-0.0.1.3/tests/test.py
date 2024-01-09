# Setup
import os
import sys
import importlib
import bnw_tools

bnw_tools_spec = importlib.util.find_spec('bnw_tools')
if bnw_tools_spec is None:
    # use development version
    sys.path.append(os.getcwd())
    import bnw_tools

from bnw_tools.publish.Obsidian import nlped_whispered_folder
from bnw_tools.publish import util_wordcloud
from bnw_tools.extract.nlp import util_nlp

folder_path = "D:/workspace/Zotero/SE2A-B4-2"
language = "en"

nlptools = util_nlp.NLPTools()

# NLP (Flair and SpaCy)
folder = util_nlp.Folder(
    folder_path, nlptools=nlptools, language=language)

# Wordcloud
if folder.media_resources:
    util_wordcloud.generate_wordcloud(
        folder.bag_of_words.get(), os.path.join(folder_path, "00_bag_of_words"))
    util_wordcloud.generate_wordcloud(
        folder.named_entities.get_frequencies(), os.path.join(folder_path, "00_named_entities"))
    mask_path = folder.get_image()
    if mask_path:
        mask = util_wordcloud.generate_mask(mask_path)
        util_wordcloud.generate_wordcloud_mask(
            folder.bag_of_words.get(), mask, os.path.join(folder_path, "00_bag_of_words_mask"))
        util_wordcloud.generate_wordcloud_mask(folder.named_entities.get_frequencies(
        ), mask, os.path.join(folder_path, "00_named_entities_mask"))

    # Obsidian
    nlped_whispered_folder.folder(folder, force=True)
