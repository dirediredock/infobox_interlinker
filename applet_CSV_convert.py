# by Matias I. Bofarull Oddo - 2022.11.06

import json
import pandas as pd


def remove_duplicates(list_rray):
    unique_rows = []
    for row in sorted(list_rray):
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows


def CSV_convert(name_string):

    with open("network_data_" + name_string + ".json") as json_file:
        wikigraph = json.load(json_file)
    json_file.close()

    collect_no_infobox = []
    list_true_href = []

    for key, fields in wikigraph.items():
        if fields == {}:
            collect_no_infobox.append(key)
        else:
            list_true_href.append(
                [
                    key,
                    wikigraph[key]["true_href"],
                    wikigraph[key]["match"],
                ]
            )

    df_true_href = pd.DataFrame(
        sorted((list_true_href)),
        columns=["href", "true_href", "match"],
    )
    mismatch_href = df_true_href.loc[df_true_href["match"] == "False"]
    mismatch_href = mismatch_href.drop("match", axis=1)
    mismatch_dict = {}
    for row in mismatch_href.to_numpy():
        if row[0] not in mismatch_dict:
            mismatch_dict[row[0]] = row[1]

    directed_incoming = []
    directed_outgoing = []

    for key, fields in wikigraph.items():

        if fields != {}:

            list_incoming = fields.get("incoming")
            for incoming_href in list_incoming:
                directed_incoming.append(
                    [
                        mismatch_dict.get(key)
                        if mismatch_dict.get(key) != None
                        else key,
                        mismatch_dict.get(incoming_href)
                        if mismatch_dict.get(incoming_href) != None
                        else incoming_href,
                    ]
                )

            list_outgoing = fields.get("outgoing")
            for outgoing_href in list_outgoing:
                directed_outgoing.append(
                    [
                        mismatch_dict.get(key)
                        if mismatch_dict.get(key) != None
                        else key,
                        mismatch_dict.get(outgoing_href)
                        if mismatch_dict.get(outgoing_href) != None
                        else outgoing_href,
                    ]
                )

    collect_infobox = []

    for row in directed_incoming:
        for href in row:
            collect_infobox.append(href)
    for row in directed_outgoing:
        for href in row:
            collect_infobox.append(href)

    list_infobox = set(collect_infobox)
    list_no_infobox = set(collect_no_infobox)

    df_list_infobox = pd.DataFrame(
        sorted(list_infobox),
        columns=["href"],
    )
    df_list_no_infobox = pd.DataFrame(
        sorted(list_no_infobox),
        columns=["href"],
    )

    df_list_infobox["infobox"] = True
    df_list_no_infobox["infobox"] = False

    list_nodes = df_list_infobox.append(df_list_no_infobox, ignore_index=True)
    list_nodes.to_csv(
        "list_nodes_" + name_string + ".tsv",
        index=False,
        sep="\t",
    )

    df_directed_incoming = pd.DataFrame(
        remove_duplicates(directed_incoming),
        columns=["href", "incoming_href"],
    )
    df_directed_incoming.sort_values(by=["href"], inplace=True)
    df_directed_incoming.to_csv(
        "directed_incoming_" + name_string + ".tsv",
        index=False,
        sep="\t",
    )

    df_directed_outgoing = pd.DataFrame(
        remove_duplicates(directed_outgoing),
        columns=["href", "outgoing_href"],
    )
    df_directed_outgoing.sort_values(by=["href"], inplace=True)
    df_directed_outgoing.to_csv(
        "directed_outgoing_" + name_string + ".tsv",
        index=False,
        sep="\t",
    )

    print()
    print(name_string)
    print()
    print("\tNodes\t\t\t")
    print(
        "\t\ttotal\t\t\t",
        len(list_infobox) + len(list_no_infobox),
    )
    print(
        "\t\twith infobox\t\t",
        len(list_infobox),
    )
    print(
        "\t\twithout infobox\t\t",
        len(list_no_infobox),
    )
    print("\tEdges\t\t\t")
    print(
        "\t\tincoming graph\t\t",
        len(directed_incoming),
    )
    print(
        "\t\toutgoing graph\t\t",
        len(directed_outgoing),
    )
    print()
