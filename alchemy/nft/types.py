from __future__ import annotations

import enum
from typing import TypedDict, List, Union, Literal, Any, Optional

from web3.types import ENS

from alchemy.exceptions import AlchemyError
from alchemy.types import HexAddress

from typing_extensions import NotRequired, Required


NftExcludeFilters = Literal['SPAM', 'AIRDROPS']
TokenID = Union[str, int]
NftSpamClassification = Literal[
    'Erc721TooManyOwners',
    'Erc721TooManyTokens',
    'Erc721DishonestTotalSupply',
    'MostlyHoneyPotOwners',
    'OwnedByMostHoneyPots',
]


class OpenSeaSafelistRequestStatus(enum.Enum):
    VERIFIED = 'verified'
    APPROVED = 'approved'
    REQUESTED = 'requested'
    NOT_REQUESTED = 'not_requested'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value).value
        except ValueError:
            return None


class NftTokenType(enum.Enum):
    ERC721 = 'ERC721'
    ERC1155 = 'ERC1155'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value).value
        except ValueError:
            return cls.UNKNOWN.value


class NftMetadataParams(TypedDict, total=False):
    contractAddress: Required[HexAddress]
    tokenId: Required[str]
    tokenType: NftTokenType
    refreshCache: bool
    tokenUriTimeoutInMs: int


class BaseNftContract(TypedDict):
    address: HexAddress


class OpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: float
    collectionName: str
    safelistRequestStatus: Required[OpenSeaSafelistRequestStatus]
    imageUrl: str
    description: str
    externalUrl: str
    twitterUsername: str
    discordUrl: str
    lastIngestedAt: str


class NftContract(BaseNftContract, total=False):
    tokenType: Required[NftTokenType]
    name: Optional[str]
    symbol: Optional[str]
    totalSupply: Optional[str]
    openSea: OpenSeaCollectionMetadata


class BaseNft(TypedDict):
    contract: BaseNftContract
    tokenId: str
    tokenType: NftTokenType


class NftMetadata(TypedDict, total=False):
    name: str
    description: str
    image: str
    external_url: str
    background_color: str
    attributes: List[Any]


class TokenUri(TypedDict):
    raw: str
    gateway: str


class Media(TypedDict, total=False):
    raw: Required[str]
    gateway: Required[str]
    thumbnail: str
    format: str
    bytes: int


class SpamInfo(TypedDict):
    isSpam: bool
    classifications: List[NftSpamClassification]


class Nft(TypedDict):
    contract: NftContract
    tokenId: str
    tokenType: NftTokenType
    title: str
    description: str
    timeLastUpdated: str
    metadataError: Optional[str]
    rawMetadata: Optional[NftMetadata]
    tokenUri: Optional[TokenUri]
    media: List[Media]
    spamInfo: NotRequired[SpamInfo]


class OwnedNft(Nft):
    balance: int


class OwnedBaseNft(BaseNft):
    balance: int


class OwnedNftsResponse(TypedDict):
    ownedNfts: List[OwnedNft]
    pageKey: NotRequired[str]
    totalCount: int


class OwnedBaseNftsResponse(TypedDict):
    ownedNfts: List[OwnedBaseNft]
    pageKey: NotRequired[str]
    totalCount: int


class NftsForOwnerOptions(TypedDict, total=False):
    pageKey: str
    contractAddresses: List[HexAddress]
    excludeFilters: List[NftExcludeFilters]
    pageSize: int
    omitMetadata: bool
    tokenUriTimeoutInMs: int


class BaseNftsForOwnerOptions(TypedDict, total=False):
    pageKey: str
    contractAddresses: List[HexAddress]
    excludeFilters: List[NftExcludeFilters]
    pageSize: int
    omitMetadata: Required[Literal[True]]
    tokenUriTimeoutInMs: int


NftsAlchemyParams = TypedDict(
    'NftsAlchemyParams',
    {
        'owner': Required[Union[HexAddress, ENS]],
        'pageKey': str,
        'contractAddresses': List[HexAddress],
        'filters[]': List[str],
        'pageSize': int,
        'withMetadata': Required[bool],
        'tokenUriTimeoutInMs': int,
    },
    total=False,
)


class ContractMetadataParams(TypedDict):
    contractAddress: HexAddress


class NftsForContractOptions(TypedDict, total=False):
    pageKey: str
    omitMetadata: bool
    pageSize: int
    tokenUriTimeoutInMs: int


class BaseNftsForContractOptions(TypedDict, total=False):
    pageKey: str
    omitMetadata: Required[Literal[False]]
    pageSize: int
    tokenUriTimeoutInMs: int


class NftContractNftsResponse(TypedDict):
    nfts: List[Nft]
    pageKey: NotRequired[str]


class NftContractBaseNftsResponse(TypedDict):
    nfts: List[BaseNft]
    pageKey: NotRequired[str]


class NftsForContractAlchemyParams(TypedDict, total=False):
    contractAddress: Required[HexAddress]
    startToken: str
    withMetadata: Required[bool]
    limit: int
    tokenUriTimeoutInMs: int


class OwnersForNftResponse(TypedDict):
    owners: List[str]


class OwnersForContractOptions(TypedDict, total=False):
    withTokenBalances: bool
    block: str
    pageKey: str


class OwnersForContractWithTokenBalancesOptions(TypedDict, total=False):
    withTokenBalances: Required[Literal[True]]
    block: str
    pageKey: str


class OwnersForContractResponse(TypedDict):
    owners: List[str]


class NftContractTokenBalance(TypedDict):
    tokenId: str
    balance: float


class NftContractOwner(TypedDict):
    ownerAddress: HexAddress
    tokenBalances: List[NftContractTokenBalance]


class OwnersForContractWithTokenBalancesResponse(TypedDict):
    owners: List[NftContractOwner]
    pageKey: NotRequired[str]


class RefreshState(enum.Enum):
    DOES_NOT_EXIST = 'does_not_exist'
    ALREADY_QUEUED = 'already_queued'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    QUEUED = 'queued'
    QUEUE_FAILED = 'queue_failed'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value).value
        except ValueError:
            raise AlchemyError(f'Unknown reingestion state: {value}')


class RefreshContractResult(TypedDict):
    contractAddress: HexAddress
    refreshState: RefreshState
    progress: Optional[str]


class FloorPriceMarketplace(TypedDict):
    floorPrice: float
    priceCurrency: str
    collectionUrl: str
    retrievedAt: str


class FloorPriceError(TypedDict):
    error: str


class FloorPriceResponse(TypedDict):
    openSea: FloorPriceMarketplace | FloorPriceError
    looksRare: FloorPriceMarketplace | FloorPriceError


class NftAttributeRarity(TypedDict):
    value: str
    traitType: str
    prevalence: int


class RawNftTokenMetadata(TypedDict):
    tokenType: NftTokenType


class RawNftId(TypedDict):
    tokenId: str
    tokenMetadata: NotRequired[RawNftTokenMetadata]


class RawOpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: float
    collectionName: str
    safelistRequestStatus: str
    imageUrl: str
    description: str
    externalUrl: str
    twitterUsername: str
    discordUrl: str
    lastIngestedAt: str


class RawNftContractMetadata(TypedDict, total=False):
    name: str
    symbol: str
    totalSupply: str
    tokenType: NftTokenType
    openSea: RawOpenSeaCollectionMetadata


class RawSpamInfo(TypedDict):
    isSpam: str
    classifications: List[NftSpamClassification]


class RawBaseNft(TypedDict):
    contract: BaseNftContract
    id: RawNftId


class RawOwnedBaseNft(RawBaseNft):
    balance: str


class RawNft(RawBaseNft, total=False):
    title: Required[str]
    description: str | List[str]
    tokenUri: TokenUri
    media: List[Media]
    metadata: NftMetadata
    timeLastUpdated: Required[str]
    error: str
    contractMetadata: RawNftContractMetadata
    spamInfo: RawSpamInfo


class RawOwnedNft(RawNft):
    balance: str


class RawBaseNftsResponse(TypedDict):
    ownedNfts: List[RawOwnedBaseNft]
    pageKey: NotRequired[str]
    totalCount: int


class RawNftsResponse(TypedDict):
    ownedNfts: List[RawOwnedNft]
    pageKey: NotRequired[str]
    totalCount: int


class RawNftContract(TypedDict):
    address: HexAddress
    contractMetadata: RawNftContractMetadata


class RawContractBaseNft(TypedDict):
    id: RawNftId


class RawNftsForContractResponse(TypedDict):
    nfts: List[RawContractBaseNft]
    nextToken: NotRequired[str]


class RawBaseNftsForContractResponse(TypedDict):
    nfts: List[RawNft]
    nextToken: NotRequired[str]


class RawReingestContractResponse(TypedDict):
    contractAddress: HexAddress
    reingestionState: str
    progress: Optional[str]


class RawNftAttributeRarity(TypedDict):
    value: str
    trait_type: str
    prevalence: int
