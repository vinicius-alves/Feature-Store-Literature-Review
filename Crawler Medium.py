import requests, json
import pandas as pd
from tqdm.notebook import tqdm
from datetime import datetime


url = 'https://medium.com/_/graphql'

data = [
  {
    "operationName": "SearchQuery",
    "variables": {
      "query": "feature store",
      "pagingOptions": {
        "limit": 10,
        "page": 1
      },
      "withUsers": False,
      "withTags": False,
      "withPosts": True,
      "withCollections": False,
      "withLists": False,
      "peopleSearchOptions": {
        "filters": "highQualityUser:true OR writtenByHighQulityUser:true",
        "numericFilters": "peopleType!=2",
        "clickAnalytics": True,
        "analyticsTags": [
          "web-main-content"
        ]
      },
      "postsSearchOptions": {
        "filters": "writtenByHighQualityUser:true",
        "clickAnalytics": True,
        "analyticsTags": [
          "web-main-content"
        ]
      },
      "publicationsSearchOptions": {
        "clickAnalytics": True,
        "analyticsTags": [
          "web-main-content"
        ]
      },
      "tagsSearchOptions": {
        "numericFilters": "postCount>=1",
        "clickAnalytics": True,
        "analyticsTags": [
          "web-main-content"
        ]
      },
      "listsSearchOptions": {
        "clickAnalytics": True,
        "analyticsTags": [
          "web-main-content"
        ]
      },
      "searchInCollection": False,
      "collectionDomainOrSlug": "medium.com"
    },
    "query": "query SearchQuery($query: String!, $pagingOptions: SearchPagingOptions!, $searchInCollection: Boolean!, $collectionDomainOrSlug: String!, $withUsers: Boolean!, $withTags: Boolean!, $withPosts: Boolean!, $withCollections: Boolean!, $withLists: Boolean!, $peopleSearchOptions: SearchOptions, $postsSearchOptions: SearchOptions, $tagsSearchOptions: SearchOptions, $publicationsSearchOptions: SearchOptions, $listsSearchOptions: SearchOptions) {\n  search(query: $query) @skip(if: $searchInCollection) {\n    __typename\n    ...Search_search\n  }\n  searchInCollection(query: $query, domainOrSlug: $collectionDomainOrSlug) @include(if: $searchInCollection) {\n    __typename\n    ...Search_search\n  }\n}\n\nfragment Search_search on Search {\n  people(pagingOptions: $pagingOptions, algoliaOptions: $peopleSearchOptions) @include(if: $withUsers) {\n    ... on SearchPeople {\n      pagingInfo {\n        next {\n          limit\n          page\n          __typename\n        }\n        __typename\n      }\n      ...SearchPeople_people\n      __typename\n    }\n    __typename\n  }\n  tags(pagingOptions: $pagingOptions, algoliaOptions: $tagsSearchOptions) @include(if: $withTags) {\n    ... on SearchTag {\n      pagingInfo {\n        next {\n          limit\n          page\n          __typename\n        }\n        __typename\n      }\n      ...SearchTags_tags\n      __typename\n    }\n    __typename\n  }\n  posts(pagingOptions: $pagingOptions, algoliaOptions: $postsSearchOptions) @include(if: $withPosts) {\n    ... on SearchPost {\n      pagingInfo {\n        next {\n          limit\n          page\n          __typename\n        }\n        __typename\n      }\n      ...SearchPosts_posts\n      __typename\n    }\n    __typename\n  }\n  collections(\n    pagingOptions: $pagingOptions\n    algoliaOptions: $publicationsSearchOptions\n  ) @include(if: $withCollections) {\n    ... on SearchCollection {\n      pagingInfo {\n        next {\n          limit\n          page\n          __typename\n        }\n        __typename\n      }\n      ...SearchCollections_collections\n      __typename\n    }\n    __typename\n  }\n  catalogs(pagingOptions: $pagingOptions, algoliaOptions: $listsSearchOptions) @include(if: $withLists) {\n    ... on SearchCatalog {\n      pagingInfo {\n        next {\n          limit\n          page\n          __typename\n        }\n        __typename\n      }\n      ...SearchLists_catalogs\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SearchPeople_people on SearchPeople {\n  items {\n    __typename\n    ... on User {\n      algoliaObjectId\n      __typename\n      id\n    }\n    ...UserFollowInline_user\n  }\n  queryId\n  __typename\n}\n\nfragment UserFollowInline_user on User {\n  id\n  name\n  bio\n  mediumMemberAt\n  ...UserAvatar_user\n  ...UserFollowButton_user\n  ...userUrl_user\n  ...useIsVerifiedBookAuthor_user\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment UserFollowButton_user on User {\n  ...UserFollowButtonSignedIn_user\n  ...UserFollowButtonSignedOut_user\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedIn_user on User {\n  id\n  name\n  __typename\n}\n\nfragment UserFollowButtonSignedOut_user on User {\n  id\n  ...SusiClickable_user\n  __typename\n}\n\nfragment SusiClickable_user on User {\n  ...SusiContainer_user\n  __typename\n  id\n}\n\nfragment SusiContainer_user on User {\n  ...SignInOptions_user\n  ...SignUpOptions_user\n  __typename\n  id\n}\n\nfragment SignInOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment useIsVerifiedBookAuthor_user on User {\n  verifications {\n    isBookAuthor\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment SearchTags_tags on SearchTag {\n  items {\n    id\n    algoliaObjectId\n    ...TopicPill_tag\n    __typename\n  }\n  queryId\n  __typename\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n  normalizedTagSlug\n}\n\nfragment SearchPosts_posts on SearchPost {\n  items {\n    id\n    algoliaObjectId\n    ...PostPreview_post\n    __typename\n  }\n  queryId\n  __typename\n}\n\nfragment PostPreview_post on Post {\n  id\n  creator {\n    ...PostPreview_user\n    __typename\n    id\n  }\n  collection {\n    ...CardByline_collection\n    ...ExpandablePostByline_collection\n    __typename\n    id\n  }\n  ...InteractivePostBody_postPreview\n  firstPublishedAt\n  isLocked\n  isSeries\n  latestPublishedAt\n  inResponseToCatalogResult {\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  previewImage {\n    id\n    focusPercentX\n    focusPercentY\n    __typename\n  }\n  readingTime\n  sequence {\n    slug\n    __typename\n  }\n  title\n  uniqueSlug\n  visibility\n  ...CardByline_post\n  ...PostFooterActionsBar_post\n  ...InResponseToEntityPreview_post\n  ...PostScrollTracker_post\n  ...ReadMore_post\n  ...HighDensityPreview_post\n  __typename\n}\n\nfragment PostPreview_user on User {\n  __typename\n  name\n  username\n  ...CardByline_user\n  ...ExpandablePostByline_user\n  id\n}\n\nfragment CardByline_user on User {\n  __typename\n  id\n  name\n  username\n  mediumMemberAt\n  socialStats {\n    followerCount\n    __typename\n  }\n  ...useIsVerifiedBookAuthor_user\n  ...userUrl_user\n  ...UserMentionTooltip_user\n}\n\nfragment UserMentionTooltip_user on User {\n  id\n  name\n  username\n  bio\n  imageId\n  mediumMemberAt\n  ...UserAvatar_user\n  ...UserFollowButton_user\n  ...useIsVerifiedBookAuthor_user\n  __typename\n}\n\nfragment ExpandablePostByline_user on User {\n  __typename\n  id\n  name\n  imageId\n  ...userUrl_user\n  ...useIsVerifiedBookAuthor_user\n}\n\nfragment CardByline_collection on Collection {\n  name\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment ExpandablePostByline_collection on Collection {\n  __typename\n  id\n  name\n  domain\n  slug\n}\n\nfragment InteractivePostBody_postPreview on Post {\n  extendedPreviewContent(\n    truncationConfig: {previewParagraphsWordCountThreshold: 400, minimumWordLengthForTruncation: 150, truncateAtEndOfSentence: true, showFullImageCaptions: true, shortformPreviewParagraphsWordCountThreshold: 30, shortformMinimumWordLengthForTruncation: 30}\n  ) {\n    bodyModel {\n      ...PostBody_bodyModel\n      __typename\n    }\n    isFullContent\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment PostBody_bodyModel on RichText {\n  sections {\n    name\n    startIndex\n    textLayout\n    imageLayout\n    backgroundImage {\n      id\n      originalHeight\n      originalWidth\n      __typename\n    }\n    videoLayout\n    backgroundVideo {\n      videoId\n      originalHeight\n      originalWidth\n      previewImageId\n      __typename\n    }\n    __typename\n  }\n  paragraphs {\n    id\n    ...PostBodySection_paragraph\n    __typename\n  }\n  ...normalizedBodyModel_richText\n  __typename\n}\n\nfragment PostBodySection_paragraph on Paragraph {\n  name\n  ...PostBodyParagraph_paragraph\n  __typename\n  id\n}\n\nfragment PostBodyParagraph_paragraph on Paragraph {\n  name\n  type\n  ...ImageParagraph_paragraph\n  ...TextParagraph_paragraph\n  ...IframeParagraph_paragraph\n  ...MixtapeParagraph_paragraph\n  ...CodeBlockParagraph_paragraph\n  __typename\n  id\n}\n\nfragment ImageParagraph_paragraph on Paragraph {\n  href\n  layout\n  metadata {\n    id\n    originalHeight\n    originalWidth\n    focusPercentX\n    focusPercentY\n    alt\n    __typename\n  }\n  ...Markups_paragraph\n  ...ParagraphRefsMapContext_paragraph\n  ...PostAnnotationsMarker_paragraph\n  __typename\n  id\n}\n\nfragment Markups_paragraph on Paragraph {\n  name\n  text\n  hasDropCap\n  dropCapImage {\n    ...MarkupNode_data_dropCapImage\n    __typename\n    id\n  }\n  markups {\n    type\n    start\n    end\n    href\n    anchorType\n    userId\n    linkMetadata {\n      httpStatus\n      __typename\n    }\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment MarkupNode_data_dropCapImage on ImageMetadata {\n  ...DropCap_image\n  __typename\n  id\n}\n\nfragment DropCap_image on ImageMetadata {\n  id\n  originalHeight\n  originalWidth\n  __typename\n}\n\nfragment ParagraphRefsMapContext_paragraph on Paragraph {\n  id\n  name\n  text\n  __typename\n}\n\nfragment PostAnnotationsMarker_paragraph on Paragraph {\n  ...PostViewNoteCard_paragraph\n  __typename\n  id\n}\n\nfragment PostViewNoteCard_paragraph on Paragraph {\n  name\n  __typename\n  id\n}\n\nfragment TextParagraph_paragraph on Paragraph {\n  type\n  hasDropCap\n  codeBlockMetadata {\n    mode\n    lang\n    __typename\n  }\n  ...Markups_paragraph\n  ...ParagraphRefsMapContext_paragraph\n  __typename\n  id\n}\n\nfragment IframeParagraph_paragraph on Paragraph {\n  type\n  iframe {\n    mediaResource {\n      id\n      iframeSrc\n      iframeHeight\n      iframeWidth\n      title\n      __typename\n    }\n    __typename\n  }\n  layout\n  ...Markups_paragraph\n  __typename\n  id\n}\n\nfragment MixtapeParagraph_paragraph on Paragraph {\n  type\n  mixtapeMetadata {\n    href\n    mediaResource {\n      mediumCatalog {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ...GenericMixtapeParagraph_paragraph\n  __typename\n  id\n}\n\nfragment GenericMixtapeParagraph_paragraph on Paragraph {\n  text\n  mixtapeMetadata {\n    href\n    thumbnailImageId\n    __typename\n  }\n  markups {\n    start\n    end\n    type\n    href\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment CodeBlockParagraph_paragraph on Paragraph {\n  codeBlockMetadata {\n    lang\n    mode\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment normalizedBodyModel_richText on RichText {\n  paragraphs {\n    ...normalizedBodyModel_richText_paragraphs\n    __typename\n  }\n  sections {\n    startIndex\n    ...getSectionEndIndex_section\n    __typename\n  }\n  ...getParagraphStyles_richText\n  ...getParagraphSpaces_richText\n  __typename\n}\n\nfragment normalizedBodyModel_richText_paragraphs on Paragraph {\n  markups {\n    ...normalizedBodyModel_richText_paragraphs_markups\n    __typename\n  }\n  codeBlockMetadata {\n    lang\n    mode\n    __typename\n  }\n  ...getParagraphHighlights_paragraph\n  ...getParagraphPrivateNotes_paragraph\n  __typename\n  id\n}\n\nfragment normalizedBodyModel_richText_paragraphs_markups on Markup {\n  type\n  __typename\n}\n\nfragment getParagraphHighlights_paragraph on Paragraph {\n  name\n  __typename\n  id\n}\n\nfragment getParagraphPrivateNotes_paragraph on Paragraph {\n  name\n  __typename\n  id\n}\n\nfragment getSectionEndIndex_section on Section {\n  startIndex\n  __typename\n}\n\nfragment getParagraphStyles_richText on RichText {\n  paragraphs {\n    text\n    type\n    __typename\n  }\n  sections {\n    ...getSectionEndIndex_section\n    __typename\n  }\n  __typename\n}\n\nfragment getParagraphSpaces_richText on RichText {\n  paragraphs {\n    layout\n    metadata {\n      originalHeight\n      originalWidth\n      id\n      __typename\n    }\n    type\n    ...paragraphExtendsImageGrid_paragraph\n    __typename\n  }\n  ...getSeriesParagraphTopSpacings_richText\n  ...getPostParagraphTopSpacings_richText\n  __typename\n}\n\nfragment paragraphExtendsImageGrid_paragraph on Paragraph {\n  layout\n  type\n  __typename\n  id\n}\n\nfragment getSeriesParagraphTopSpacings_richText on RichText {\n  paragraphs {\n    id\n    __typename\n  }\n  sections {\n    ...getSectionEndIndex_section\n    __typename\n  }\n  __typename\n}\n\nfragment getPostParagraphTopSpacings_richText on RichText {\n  paragraphs {\n    type\n    layout\n    text\n    codeBlockMetadata {\n      lang\n      mode\n      __typename\n    }\n    __typename\n  }\n  sections {\n    ...getSectionEndIndex_section\n    __typename\n  }\n  __typename\n}\n\nfragment CardByline_post on Post {\n  ...DraftStatus_post\n  ...Star_post\n  ...shouldShowPublishedInStatus_post\n  __typename\n  id\n}\n\nfragment DraftStatus_post on Post {\n  id\n  pendingCollection {\n    id\n    creator {\n      id\n      __typename\n    }\n    ...BoldCollectionName_collection\n    __typename\n  }\n  statusForCollection\n  creator {\n    id\n    __typename\n  }\n  isPublished\n  __typename\n}\n\nfragment BoldCollectionName_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment Star_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment shouldShowPublishedInStatus_post on Post {\n  statusForCollection\n  isPublished\n  __typename\n  id\n}\n\nfragment PostFooterActionsBar_post on Post {\n  id\n  visibility\n  allowResponses\n  postResponses {\n    count\n    __typename\n  }\n  isLimitedState\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...MultiVote_post\n  ...PostSharePopover_post\n  ...OverflowMenuButtonWithNegativeSignal_post\n  ...PostPageBookmarkButton_post\n  __typename\n}\n\nfragment MultiVote_post on Post {\n  id\n  creator {\n    id\n    ...SusiClickable_user\n    __typename\n  }\n  isPublished\n  ...SusiClickable_post\n  collection {\n    id\n    slug\n    __typename\n  }\n  isLimitedState\n  ...MultiVoteCount_post\n  __typename\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment PostSharePopover_post on Post {\n  id\n  mediumUrl\n  title\n  isPublished\n  ...SharePostButton_post\n  ...usePostUrl_post\n  __typename\n}\n\nfragment SharePostButton_post on Post {\n  id\n  __typename\n}\n\nfragment usePostUrl_post on Post {\n  id\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  collection {\n    id\n    domain\n    slug\n    __typename\n  }\n  isSeries\n  mediumUrl\n  sequence {\n    slug\n    __typename\n  }\n  uniqueSlug\n  __typename\n}\n\nfragment OverflowMenuButtonWithNegativeSignal_post on Post {\n  id\n  visibility\n  ...OverflowMenuWithNegativeSignal_post\n  __typename\n}\n\nfragment OverflowMenuWithNegativeSignal_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...OverflowMenuItemUndoClaps_post\n  ...AddToCatalogBase_post\n  __typename\n}\n\nfragment OverflowMenuItemUndoClaps_post on Post {\n  id\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  isPublished\n  __typename\n}\n\nfragment PostPageBookmarkButton_post on Post {\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment InResponseToEntityPreview_post on Post {\n  id\n  inResponseToEntityType\n  __typename\n}\n\nfragment PostScrollTracker_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  sequence {\n    sequenceId\n    __typename\n  }\n  __typename\n}\n\nfragment ReadMore_post on Post {\n  mediumUrl\n  readingTime\n  ...usePostUrl_post\n  __typename\n  id\n}\n\nfragment HighDensityPreview_post on Post {\n  id\n  title\n  previewImage {\n    id\n    focusPercentX\n    focusPercentY\n    __typename\n  }\n  extendedPreviewContent(\n    truncationConfig: {previewParagraphsWordCountThreshold: 400, minimumWordLengthForTruncation: 150, truncateAtEndOfSentence: true, showFullImageCaptions: true, shortformPreviewParagraphsWordCountThreshold: 30, shortformMinimumWordLengthForTruncation: 30}\n  ) {\n    subtitle\n    __typename\n  }\n  ...HighDensityFooter_post\n  __typename\n}\n\nfragment HighDensityFooter_post on Post {\n  id\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...ExpandablePostCardOverflowButton_post\n  ...OverflowMenuButtonWithNegativeSignal_post\n  __typename\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment ExpandablePostCardOverflowButton_post on Post {\n  creator {\n    id\n    __typename\n  }\n  ...ExpandablePostCardReaderButton_post\n  __typename\n  id\n}\n\nfragment ExpandablePostCardReaderButton_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  creator {\n    id\n    __typename\n  }\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment SearchCollections_collections on SearchCollection {\n  items {\n    id\n    algoliaObjectId\n    ...CollectionFollowInline_collection\n    __typename\n  }\n  queryId\n  __typename\n}\n\nfragment CollectionFollowInline_collection on Collection {\n  id\n  name\n  domain\n  shortDescription\n  slug\n  ...CollectionAvatar_collection\n  ...CollectionFollowButton_collection\n  __typename\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment CollectionFollowButton_collection on Collection {\n  __typename\n  id\n  name\n  slug\n  ...collectionUrl_collection\n  ...SusiClickable_collection\n}\n\nfragment SusiClickable_collection on Collection {\n  ...SusiContainer_collection\n  __typename\n  id\n}\n\nfragment SusiContainer_collection on Collection {\n  name\n  ...SignInOptions_collection\n  ...SignUpOptions_collection\n  __typename\n  id\n}\n\nfragment SignInOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SearchLists_catalogs on SearchCatalog {\n  items {\n    id\n    algoliaObjectId\n    ...CatalogsListItem_catalog\n    __typename\n  }\n  queryId\n  __typename\n}\n\nfragment CatalogsListItem_catalog on Catalog {\n  id\n  name\n  predefined\n  visibility\n  creator {\n    imageId\n    name\n    ...userUrl_user\n    ...useIsVerifiedBookAuthor_user\n    __typename\n    id\n  }\n  ...getCatalogSlugId_Catalog\n  ...formatItemsCount_catalog\n  ...CatalogsListItemCovers_catalog\n  ...CatalogContentMenu_catalog\n  ...SaveCatalogButton_catalog\n  __typename\n}\n\nfragment getCatalogSlugId_Catalog on Catalog {\n  id\n  name\n  __typename\n}\n\nfragment formatItemsCount_catalog on Catalog {\n  postItemsCount\n  __typename\n  id\n}\n\nfragment CatalogsListItemCovers_catalog on Catalog {\n  listItemsConnection: itemsConnection(pagingOptions: {limit: 10}) {\n    items {\n      catalogItemId\n      ...PreviewCatalogCovers_catalogItemV2\n      __typename\n    }\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment PreviewCatalogCovers_catalogItemV2 on CatalogItemV2 {\n  catalogItemId\n  entity {\n    __typename\n    ... on Post {\n      visibility\n      previewImage {\n        id\n        alt\n        __typename\n      }\n      __typename\n      id\n    }\n  }\n  __typename\n}\n\nfragment CatalogContentMenu_catalog on Catalog {\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  ...CatalogContentNonCreatorMenu_catalog\n  ...CatalogContentCreatorMenu_catalog\n  __typename\n  id\n}\n\nfragment CatalogContentNonCreatorMenu_catalog on Catalog {\n  id\n  viewerEdge {\n    clapCount\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment CatalogContentCreatorMenu_catalog on Catalog {\n  id\n  visibility\n  name\n  description\n  type\n  postItemsCount\n  predefined\n  disallowResponses\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  ...UpdateCatalogDialog_catalog\n  ...catalogUrl_catalog\n  __typename\n}\n\nfragment UpdateCatalogDialog_catalog on Catalog {\n  id\n  name\n  description\n  visibility\n  type\n  __typename\n}\n\nfragment catalogUrl_catalog on Catalog {\n  id\n  predefined\n  ...getCatalogSlugId_Catalog\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment SaveCatalogButton_catalog on Catalog {\n  id\n  creator {\n    id\n    username\n    __typename\n  }\n  viewerEdge {\n    id\n    isFollowing\n    __typename\n  }\n  ...getCatalogSlugId_Catalog\n  __typename\n}\n"
  }
]


headers  = {
    'Content-Type':'application/json'
    
}
page = 1
results = []
pbar = tqdm()

while True:

    data[0]['variables']['pagingOptions']['page'] = page
    r = requests.post(url, data= json.dumps(data), headers = headers)
    result = r.json()[0]['data']['search']['posts']['items']
    results += result
    if len(result) == 0:
        break
    page += 1
    pbar.update(1)


# In[241]:


import pandas as pd
df_results = pd.DataFrame(results)

df_results = df_results[~df_results['id'].duplicated(keep= 'first')]


df_results['Autor'] = df_results['creator'].map(lambda x: x['name'])
df_results['AutorSeguidores'] = df_results['creator'].map(lambda x: x['socialStats']['followerCount'])


df_results.loc[ix,'Coleção'] = df_results.loc[ix,'collection'].map(lambda x: x['name'])

df_results['Prévia'] = df_results['extendedPreviewContent'].map(lambda x: '\n'.join([item['text'] for item \
                                                 in x['bodyModel']['paragraphs'] if item['text'] is not None]))

df_results['DataPublicação'] = df_results['firstPublishedAt'].map(lambda x : datetime.utcfromtimestamp(x/1000))
df_results= df_results[df_results['DataPublicação'].map(lambda x: x.year >= 2017)]

df_results = df_results.rename(columns = {'isSeries':'Série','readingTime':'TempoLeitura','visibility':'Visibilidade',\
                                          'mediumUrl':'URL','voterCount':'Votos','clapCount':'Palmas','title':'Título'})

df_results['Respostas'] = df_results['postResponses'].map(lambda x: x['count'])

df_results['TagsLista'] = df_results['tags'].map(lambda x: [item['displayTitle'] for item in x])

df_results = df_results[df_results['TagsLista'].map(lambda x: 'Feature Store' in x) |\
           df_results['Título'].str.lower().str.contains('feature store')]

df_results['Tags'] = df_results['TagsLista'].map(', '.join)

df_results = df_results[['URL','Título','Prévia','DataPublicação','Tags','Série', 'TempoLeitura', 'Visibilidade', 'Votos',
       'Palmas', 'Autor', 'AutorSeguidores', 'Coleção', 'Respostas']]

df_results.to_excel('Publicações_Medium.xlsx')

