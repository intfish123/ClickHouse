import pytest

from helpers.cluster import ClickHouseCluster

cluster = ClickHouseCluster(__file__)

node1 = cluster.add_instance(
    "node1",
    main_configs=["configs/clusters.xml"],
    with_zookeeper=True,
    allow_analyzer=False,
)
node2 = cluster.add_instance(
    "node2",
    main_configs=["configs/clusters.xml"],
    with_zookeeper=True,
    allow_analyzer=False,
)


@pytest.fixture(scope="module")
def start_cluster():
    try:
        cluster.start()
        yield cluster
    finally:
        cluster.shutdown()


def test_groupBitmapAndState_on_distributed_table(start_cluster):
    local_table_name = "test_group_bitmap_state"
    distributed_table_name = "test_group_bitmap_state_dst"
    cluster_name = "awesome_cluster"

    for node in (node1, node2):
        node.query(
            """CREATE TABLE {}
        (
            z AggregateFunction(groupBitmap, UInt32)
        )
        ENGINE = MergeTree()
        ORDER BY tuple()""".format(
                local_table_name
            )
        )

        node.query(
            """CREATE TABLE {}
        (
            z AggregateFunction(groupBitmap, UInt32)
        )
        ENGINE = Distributed('{}', 'default', '{}')""".format(
                distributed_table_name, cluster_name, local_table_name
            )
        )

    node1.query(
        """INSERT INTO {} VALUES
                (bitmapBuild(cast([1,2,3,4,5,6,7,8,9,10] as Array(UInt32))));""".format(
            local_table_name
        )
    )

    node2.query(
        """INSERT INTO {} VALUES
                (bitmapBuild(cast([0] as Array(UInt32))));""".format(
            local_table_name
        )
    )

    expected = "0"
    for node in (node1, node2):
        result = node.query(
            "select bitmapCardinality(groupBitmapAndState(z)) FROM {};".format(
                distributed_table_name
            )
        ).strip()
        assert result == expected
