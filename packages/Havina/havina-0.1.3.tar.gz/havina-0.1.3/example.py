from havina import GraphGenerator
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


if __name__ == '__main__':
    # source: https://en.wikipedia.org/wiki/Amsterdam
    text = ("Amsterdam was founded at the mouth of the Amstel River that was dammed to control flooding; "
            "the city's name derives from a local linguistic variation of the word dam. Originally a small fishing village "
            "in the late 12th century, Amsterdam became a major world port during the Dutch Golden Age of the 17th"
            " century, when the Netherlands was an economic powerhouse. Amsterdam was the leading centre for finance "
            "and trade, as well as a hub of production of secular art. In the 19th and 20th centuries, the city "
            "expanded and many new neighborhoods and suburbs were planned and built. The canals of Amsterdam and the "
            "19-20th century Defence Line of Amsterdam are both on the UNESCO World Heritage List. Sloten, annexed in "
            "1921 by the municipality of Amsterdam, is the oldest part of the city, dating to the 9th century. The city "
            "has a long tradition of openness, liberalism, and tolerance. Cycling is key to the city's modern character,"
            " and there are numerous biking paths and lanes spread throughout the entire city.")
    generator = GraphGenerator(forward_tokens=True, link_entity=False, top_k=6, contiguous_token=True,
                               relation_length=4, threshold=0.05)

    relations = generator(text, 4)

    for item in relations:
        print(f"{item.head.text} ------ {item.tail.text}")
        for rel in item.relations:
            print(rel)

    source: list[str] = []
    target: list[str] = []
    relation: list[str] = []

    filter_items = ['amsterdam', 'the netherlands']
    for item in relations:
        head_text = item.head.text
        tail_text = item.tail.text
        if head_text in filter_items or tail_text in filter_items:
            for rel in item.relations:
                source.append(head_text)
                target.append(tail_text)
                relation.append(rel)

    kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relation})
    G = nx.from_pandas_edgelist(kg_df, 'source', 'target', edge_attr=True, create_using=nx.MultiGraph)
    plt.figure(figsize=(12, 12))
    pos = nx.planar_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
    nx.draw_networkx_edge_labels(G, pos=pos)
    plt.show()