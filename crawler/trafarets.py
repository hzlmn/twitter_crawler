import trafaret as t
from trafaret.keys import xor_key

SettingsTrafaret = t.Dict({
    t.Key("search_phrase"): t.String(min_length=3),
    t.Key("search_interval"): t.Int(gt=0)
})


SettingsOutputTrafaret = t.Dict({
    t.Key("search_settings"): t.Or(SettingsTrafaret, t.Dict({}))
})


_StatusTrafaret = t.Dict({
    t.Key("executed_at"): t.Int(gt=0),
    t.Key("interval"): t.Int(gte=0),
    t.Key("search_phrase"): t.String,
    t.Key("statistics"): t.Dict({
        t.Key("top_hashtags"): t.List(t.String),
        t.Key("top_phrase"): t.String,
        t.Key("top_publisher"): t.String,
        t.Key("tweet_count"): t.Int
    })
})

StatusesOutputTrafaret = t.List(_StatusTrafaret)
