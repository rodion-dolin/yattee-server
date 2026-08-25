"""Regression tests for InnerTube recommendation response shapes."""

from innertube._converters import _recommended_videos_from_next


def test_direct_lockup_view_model_recommendation_is_extracted():
    """WEB /next responses may return recommendation lockups directly."""
    lockup = {
        "contentType": "LOCKUP_CONTENT_TYPE_VIDEO",
        "contentId": "neutralVideoId",
        "metadata": {
            "lockupMetadataViewModel": {
                "title": {"content": "Neutral recommendation"},
                "metadata": {
                    "contentMetadataViewModel": {
                        "metadataRows": [
                            {
                                "metadataParts": [
                                    {
                                        "text": {
                                            "content": "Example Creator",
                                            "commandRuns": [
                                                {
                                                    "onTap": {
                                                        "innertubeCommand": {
                                                            "browseEndpoint": {"browseId": "UCneutral"}
                                                        }
                                                    }
                                                }
                                            ],
                                        }
                                    }
                                ]
                            },
                            {
                                "metadataParts": [
                                    {"text": {"content": "1.2K views"}},
                                    {"text": {"content": "2 days ago"}},
                                ]
                            },
                        ]
                    }
                },
            }
        },
        "contentImage": {
            "thumbnailViewModel": {
                "overlays": [
                    {
                        "thumbnailOverlayBadgeViewModel": {
                            "thumbnailBadges": [{"thumbnailBadgeViewModel": {"text": "3:21"}}]
                        }
                    }
                ]
            }
        },
    }
    response = {
        "contents": {
            "twoColumnWatchNextResults": {
                "secondaryResults": {"secondaryResults": {"results": [{"lockupViewModel": lockup}]}}
            }
        }
    }

    recommendations = _recommended_videos_from_next(response)

    assert len(recommendations) == 1
    assert recommendations[0]["videoId"] == "neutralVideoId"
    assert recommendations[0]["title"] == "Neutral recommendation"
    assert recommendations[0]["author"] == "Example Creator"
    assert recommendations[0]["authorId"] == "UCneutral"
    assert recommendations[0]["viewCount"] == 1200
    assert recommendations[0]["publishedText"] == "2 days ago"
    assert recommendations[0]["lengthSeconds"] == 201
