from typedload.dataloader import Loader

from dbnomics_fetcher_toolbox.types import ResourceGroupId, ResourceId

strconstructed = {ResourceGroupId, ResourceId}
loader = Loader(strconstructed=strconstructed)
