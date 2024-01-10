from typing import List, Tuple
from dataclasses import dataclass

from datetime import datetime
import pytest
from googleads_housekeeper.adapters import repository
from googleads_housekeeper.domain import events, task
from googleads_housekeeper.services import unit_of_work, external_parsers
import googleads_housekeeper.services.exclusion_specification as exclusion_specification


@dataclass
class FakePlacement:
    campaign_id: int = 1
    campaign_name: str = "01_test_campaign"
    placement: str = "example.com"
    clicks: int = 10
    ctr: float = 0.4
    placement_type: str = "WEBSITE"


@pytest.fixture
def placement():
    return FakePlacement()


class TestAdsExclusionSpecification:

    @pytest.mark.parametrize(
        "expression",
        ['single_name', 'single_name >'])
    def test_invalid_expression_length_raises_value_error(self, expression):
        with pytest.raises(ValueError, match="Incorrect expression *"):
            exclusion_specification.AdsExclusionSpecification(expression)

    def test_invalid_expression_operator_raises_value_error(self):
        with pytest.raises(ValueError, match="Incorrect operator *"):
            exclusion_specification.AdsExclusionSpecification("clicks ? 0")

    @pytest.fixture(params=[
        'clicks > 1', 'clicks = 10', 'ctr < 0.6', 'placement_type = WEBSITE',
        'placement_type contains WEB', 'campaign_name regexp ^01.+'
    ])
    def ads_exclusion_specification_success(self, request):
        return exclusion_specification.AdsExclusionSpecification(request.param)

    @pytest.fixture(params=[
        'clicks > 100', 'clicks != 10', 'ctr > 0.6',
        'placement_type = MOBILE_APPLICATION',
        'placement_type contains MOBILE', 'campaign_name regexp ^02.+'
    ])
    def ads_exclusion_specification_fail(self, request):
        return exclusion_specification.AdsExclusionSpecification(request.param)

    def test_placement_safisties_ads_exclusion_specification(
            self, placement, ads_exclusion_specification_success, bus):
        result = ads_exclusion_specification_success.is_satisfied_by(
            placement, bus.uow)
        assert result

    def test_placement_does_not_satisfy_ads_exclusion_specification(
            self, placement, ads_exclusion_specification_fail, bus):
        result = ads_exclusion_specification_fail.is_satisfied_by(
            placement, bus.uow)
        assert not result[0]

    def test_is_satisfied_by_raises_value_error_when_non_existing_entity_name_is_provided(
            self, placement, bus):
        specification = exclusion_specification.AdsExclusionSpecification(
            "fake_name > 0")
        with pytest.raises(ValueError):
            specification.is_satisfied_by(placement, bus.uow)

    def test_placement_satisfies_ads_exclusion_specifications_list(
            self, placement, bus):
        """
        If placement satisfies all exclusion specifications in the list,
        it satisfies the whole list.
        """
        spec = exclusion_specification.Specification(uow=bus.uow)
        specs = [[
            exclusion_specification.AdsExclusionSpecification('clicks > 0'),
            exclusion_specification.AdsExclusionSpecification('ctr < 1.0'),
            exclusion_specification.AdsExclusionSpecification(
                'placement_type = WEBSITE'),
        ]]

        result = spec.satisfies(specs, placement)
        assert result == ([[
            "GOOGLE_ADS_INFO:clicks > 0", "GOOGLE_ADS_INFO:ctr < 1.0",
            "GOOGLE_ADS_INFO:placement_type == WEBSITE"
        ]], {})

    def test_placement_does_not_satisfy_ads_exclusion_specifications_list(
            self, placement, bus):
        """
        If placement does not satisfy at least one exclusion specifications in the list,
        it does not satisfy the whole list.
        """
        spec = exclusion_specification.Specification(bus.uow)
        specs = [[
            exclusion_specification.AdsExclusionSpecification('clicks > 10'),
            exclusion_specification.AdsExclusionSpecification('ctr < 0.1'),
            exclusion_specification.AdsExclusionSpecification(
                'placement_type = WEBSITE'),
        ]]

        result = spec.satisfies(specs, placement)
        assert result == ([], {})


class TestContentExclusionSpecifition:

    @pytest.fixture(params=[
        'title contains games', 'description contains fun',
        'keywords regexp free'
    ])
    def content_exclusion_specification_success(self, request):
        return exclusion_specification.ContentExclusionSpecification(
            expression=request.param)

    @pytest.fixture(params=[
        'title contains football', 'description contains gloomy',
        'keywords regexp paid'
    ])
    def content_exclusion_specification_failure(self, request):
        return exclusion_specification.ContentExclusionSpecification(
            expression=request.param)

    def test_website_satisfies_content_exclusion_specification(
            self, placement, content_exclusion_specification_success,
            bus):
        result = content_exclusion_specification_success.is_satisfied_by(
            placement, bus.uow)
        assert result

    def test_website_does_not_satisfy_content_exclusion_specification(
            self, placement, content_exclusion_specification_failure,
            bus):
        result = content_exclusion_specification_failure.is_satisfied_by(
            placement, bus.uow)
        assert not result[0]


class TestYouTubeChannelExclusionSpecifition:

    @pytest.fixture
    def youtube_channel_placement(self):
        return FakePlacement(placement="1kdjf0skdjfw0dsdf",
                             placement_type="YOUTUBE_CHANNEL")

    @pytest.fixture(params=[
        'title regexp garden*', 'description contains game', 'country = US',
        'viewCount > 10', 'subscriberCount > 1', 'videoCount > 1',
        'topicCategories contains game'
    ])
    def youtube_channel_exclusion_specification_success(self, request):
        return exclusion_specification.YouTubeChannelExclusionSpecification(
            expression=request.param)

    @pytest.fixture(params=[
        'title regexp football*', 'description contains tv', 'country = GB',
        'viewCount > 100000', 'subscriberCount > 100000',
        'videoCount > 100000', 'topicCategories contains football'
    ])
    def youtube_channel_exclusion_specification_failure(self, request):
        return exclusion_specification.YouTubeChannelExclusionSpecification(
            expression=request.param)

    def test_youtube_channel_satisfies_youtube_channel_exclusion_specification(
            self, youtube_channel_placement,
            youtube_channel_exclusion_specification_success, bus):
        result = youtube_channel_exclusion_specification_success.is_satisfied_by(
            youtube_channel_placement, bus.uow)
        assert result

    def test_youtube_channel_does_not_satisfy_youtube_channel_exclusion_specification(
            self, youtube_channel_placement,
            youtube_channel_exclusion_specification_failure, bus):
        result = youtube_channel_exclusion_specification_failure.is_satisfied_by(
            youtube_channel_placement, bus.uow)
        assert not result[0]


class TestYouTubeVideoExclusionSpecifition:

    @pytest.fixture
    def youtube_video_placement(self):
        return FakePlacement(placement="jojoh", placement_type="YOUTUBE_VIDEO")

    @pytest.fixture(params=[
        'title regexp garden*', 'description contains game',
        'defaultLanguage = en', 'defaultAudioLanguage = en',
        'commentCount > 1', 'favouriteCount > 1', 'likeCount > 1',
        'viewCount > 10', 'madeForKids = True',
        'topicCategories contains game', 'tags contains garden'
    ])
    def youtube_video_exclusion_specification_success(self, request):
        return exclusion_specification.YouTubeVideoExclusionSpecification(
            expression=request.param)

    @pytest.fixture(params=[
        'title regexp football*', 'description contains football',
        'defaultLanguage = es', 'defaultAudioLanguage = es',
        'commentCount > 10000', 'favouriteCount > 10000', 'likeCount > 10000',
        'viewCount > 1000000', 'madeForKids = False',
        'topicCategories contains football', 'tags contains football'
    ])
    def youtube_video_exclusion_specification_failure(self, request):
        return exclusion_specification.YouTubeVideoExclusionSpecification(
            expression=request.param)

    def test_youtube_video_satisfies_youtube_video_exclusion_specification(
            self, youtube_video_placement,
            youtube_video_exclusion_specification_success, bus):
        result = youtube_video_exclusion_specification_success.is_satisfied_by(
            youtube_video_placement, bus.uow)
        assert result

    def test_youtube_video_does_not_satisfy_youtube_video_exclusion_specification(
            self, youtube_video_placement,
            youtube_video_exclusion_specification_failure, bus):
        result = youtube_video_exclusion_specification_failure.is_satisfied_by(
            youtube_video_placement, bus.uow)
        assert not result[0]
