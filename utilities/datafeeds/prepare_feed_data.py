from utilities.model_utilities.get_all_models import get_all_models
from utilities.datafeeds.get_all_sector_data import get_all_sector_data
from utilities.datafeeds.get_feature_sets_for_pred import get_feature_sets_for_pred
from utilities.datafeeds.get_feed_data import get_feed_data


def prepare_feed_data():
  models = get_all_models()
  sector_data= get_all_sector_data()
  feature_sets, datasets = get_feature_sets_for_pred(sector_data)
  feed_data = get_feed_data(models, datasets, feature_sets)
  return feed_data