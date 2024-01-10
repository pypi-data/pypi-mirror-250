# metrics for measuring importance of characters or actors in the story
AGENT_PROMINENCE_METRICS = ['Subject frequency', 'Subject frequency (normalized)']
SFREQ_METRIC = 'Subject frequency'
SFREQ_NORM_METRIC = 'Subject frequency (normalized)'
# list of punctuation characters
PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
# name of storynavigator package directory
MAIN_PACKAGE = "storynavigation"
# directory name for resource files for usage by storynavigator add-on
RESOURCES_SUBPACKAGE = "resources"
# filename from which to retrieve a list of dutch stopwords
NL_STOPWORDS_FILENAME = "dutchstopwords.txt"
# filename from which to retrieve a list of dutch past tense verbs
NL_PAST_TENSE_FILENAME = "past_tense_verbs_dutch.txt"
# filename from which to retrieve a list of dutch present tense verbs
NL_PRESENT_TENSE_FILENAME = "present_tense_verbs_dutch.txt"
# filename from which to retrieve a list of dutch false positive verbs
NL_FALSE_POSITIVE_VERB_FILENAME = "false_positive_verbs.txt"
# filename from which to retrieve a list of dutch stopwords
NL_PRONOUNS_FILENAME = "dutchpronouns.txt"
# currently selected agent prominence metric
SELECTED_PROMINENCE_METRIC = 'Subject frequency'
# column names for agency table
FREQ_TABLE_HEADER = ['actor', 'raw_frequency']
ACTION_FREQ_TABLE_HEADER = ['action', 'raw_frequency']
ACTION_TENSEFREQ_TABLE_HEADER = ['tense', 'frequency']
SUBFREQ_TABLE_HEADER = ['actor', 'subject_frequency']
CUSTOMFREQ_TABLE_HEADER = ['category', 'frequency', 'category-level']
AGENCY_TABLE_HEADER = ['actor', 'agency']
# Halliday dimensions file
HALLIDAY_FILENAME = "halliday_dimensions_{}.json"
# dutch spacy model (small)
NL_SPACY_MODEL = "nl_core_news_sm"
# colors for highlighting words in text
SUBJECT_PRONOUN_HIGHLIGHT_COLOR = "#87CEFA"
SUBJECT_NONPRONOUN_HIGHLIGHT_COLOR = "#ADD8E6"
NONSUBJECT_PRONOUN_HIGHLIGHT_COLOR = "#FFA500"
NONSUBJECT_NONPRONOUN_HIGHLIGHT_COLOR = "#FFE4B5"
ACTION_PAST_HIGHLIGHT_COLOR = "#FFC0CB"
ACTION_PRESENT_HIGHLIGHT_COLOR = "#DB7093"
CUSTOMTAG_HIGHLIGHT_COLOR = "#98FB98"

# test data file
TEST_DATA_FILE_NAME = "storynavigator-testdata.tab"
