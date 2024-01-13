# FROM BisectionController.__init__()


# if dimension_selector is None:
#     dimension_selector = select_median_low
# self._dimension_selector = dimension_selector

# self._root_partition_dimensions = dimensions

# if partition_id_builder is None:
#     partition_id_builder = hash_dimensions
# self._partition_id_builder = partition_id_builder

# if series_mask_builder is None:
#     series_mask_builder = SeriesMaskBuilder()
# self._series_mask_builder = series_mask_builder

# first_partition_attempt = PartitionAttempt(
#     depth=0,
#     dimensions=dimensions,
#     partition_id=self._partition_id_builder(dimensions),
#     series_mask=self._series_mask_builder.build_series_mask(dimensions),
# )
# self._deque: collections.deque[PartitionAttempt] = collections.deque([first_partition_attempt])


# FROM ?


# dimension_code, subpartition1_dimensions, subpartition2_dimensions = self._bisect(partition_dimensions)
# subpartition1_dimension = find_dimension_by_code(dimension_code, subpartition1_dimensions)
# subpartition2_dimension = find_dimension_by_code(dimension_code, subpartition2_dimensions)
# left_partition_attempt = PartitionAttempt(
#     depth=depth + 1,
#     dimensions=subpartition2_dimensions,
#     partition_id=self._partition_id_builder(subpartition2_dimensions),
#     series_mask=self._series_mask_builder.build_series_mask(subpartition2_dimensions),
# )
# right_partition_attempt = PartitionAttempt(
#     depth=depth + 1,
#     dimensions=subpartition1_dimensions,
#     partition_id=self._partition_id_builder(subpartition1_dimensions),
#     series_mask=self._series_mask_builder.build_series_mask(subpartition1_dimensions),
# )
# logger.debug(
#     "Dimension %r [%d] of partition #%d %r %r has been bisected in 2 partitions: %r %r [%d/%d] and %r %r [%d/%d]",  # noqa: E501
#     dimension_code,
#     len(find_dimension_by_code(dimension_code, partition_dimensions).selected_values),
#     partition_position,
#     partition_id,
#     series_mask,
#     left_partition_attempt.partition_id,
#     left_partition_attempt.series_mask,
#     len(subpartition1_dimension.selected_values),
#     subpartition1_dimension.total_num_values,
#     right_partition_attempt.partition_id,
#     right_partition_attempt.series_mask,
#     len(subpartition2_dimension.selected_values),
#     subpartition2_dimension.total_num_values,
#     depth=depth,
#     duration=format_timer(timer),
# )


# FROM BisectionController.bisect()

# def _bisect(
#     self, partition_dimensions: list[BisectDimension]
# ) -> tuple[BisectDimensionCode, list[BisectDimension], list[BisectDimension]]:
#     """Bisect ``partition_dimensions`` in two partitions.

#     Raise ``ValueError`` if ``dimensions`` are no more bisectable, i.e. all dimensions have one value left.
#     """
#     if not partition_dimensions:
#         raise NoBisectDimension

#     candidate_dimensions = [dimension for dimension in partition_dimensions if len(dimension.selected_values) > 1]
#     if not candidate_dimensions:
#         raise NoBisectableDimension(dimensions=partition_dimensions)

#     bisect_code = self._dimension_selector(candidate_dimensions)
#     bisect_dimension = find_dimension_by_code(bisect_code, partition_dimensions)
#     bisect_value_index = len(bisect_dimension.selected_values) // 2

#     def iter_bisected_dimensions() -> Iterator[tuple[BisectDimension, BisectDimension]]:
#         for dimension in partition_dimensions:
#             if dimension.code == bisect_code:
#                 partition1_values = dimension.selected_values[:bisect_value_index]
#                 partition2_values = dimension.selected_values[bisect_value_index:]
#                 yield (
#                     dataclasses.replace(dimension, selected_values=partition1_values),
#                     dataclasses.replace(dimension, selected_values=partition2_values),
#                 )
#             else:
#                 yield dimension, dimension

#     partition1_dimensions, partition2_dimensions = list(zip(*iter_bisected_dimensions(), strict=True))

#     return (
#         bisect_code,
#         cast(list[BisectDimension], partition1_dimensions),
#         cast(list[BisectDimension], partition2_dimensions),
#     )
