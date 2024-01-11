from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
import datetime
import seaborn as sns
import japanize_matplotlib
import networkx as nx
import logging
import requests
from dotenv import load_dotenv


class sapnet():
    # ログの設定
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    load_dotenv('./test.env')

    @staticmethod
    def array4DataFrame(array):
        sapnet.logger.debug("(0/10)Converting array to DataFrame")
        # 行番号を付与して各行の一番目に追加
        for i, row in enumerate(array, start=1):
            row[0] = f"{row[0]}_{i}"

        # Columnの一行目を取得し、ヘッダーとして再利用する
        header_list = ["name"]
        for i in range(len(array)):
            header_list.append(array[i][0])
        df = pd.DataFrame(array, columns=header_list)
        
        return df


    @staticmethod
    def DataFrame4array(df):
        sapnet.logger.debug("(0/10)Converting array to DataFrame")
        array = []
        for index, row in df.iterrows():
            data_row = [row['name']] + row.iloc[1:].tolist()
            array.append(data_row)
        return array

    
    @staticmethod
    def example_data():
        sapnet.logger.debug("(0/10)Converting array to DataFrame")
        data = [["knowledge", 0, 0.1, 0, 0.4, 0, 0.3, 0.5],
                ["knowledge", 0.1, 0, 0.4, 0, 0.6, 0, 0],
                ["knowledge", 0, 0.4, 0, 0.2, 0, 0, 0.7],
                ["knowledge", 0.4, 0, 0.2, 0, 0.1, 0, 0],
                ["knowledge", 0, 0.6, 0, 0.1, 0, 0.4, 0.2],
                ["knowledge", 0.3, 0, 0, 0, 0.4, 0, 0.6],
                ["knowledge", 0.5, 0, 0.7, 0, 0.2, 0.6, 0]]

        return data


    @staticmethod
    def example_dataframe():
        sapnet.logger.debug("(0/10)Converting array to DataFrame")
        data = [["knowledge", 0, 0.1, 0, 0.4, 0, 0.3, 0.5],
                ["knowledge", 0.1, 0, 0.4, 0, 0.6, 0, 0],
                ["knowledge", 0, 0.4, 0, 0.2, 0, 0, 0.7],
                ["knowledge", 0.4, 0, 0.2, 0, 0.1, 0, 0],
                ["knowledge", 0, 0.6, 0, 0.1, 0, 0.4, 0.2],
                ["knowledge", 0.3, 0, 0, 0, 0.4, 0, 0.6],
                ["knowledge", 0.5, 0, 0.7, 0, 0.2, 0.6, 0]]

        df = sapnet.array4DataFrame(data)
        
        return df

    @staticmethod
    def create_gitignore():
        gitignore_path = '.gitignore'
        # .gitignore ファイルの内容
        gitignore_content = "# api keys\n.env\n"

        # 既に .gitignore ファイルが存在する場合は処理を停止
        if os.path.exists(gitignore_path):
            print(f"{gitignore_path} ファイルは既に存在しています。処理を停止します。")
            return

        try:
            # .gitignore ファイルを作成し、内容を書き込む
            with open(gitignore_path, 'w') as gitignore_file:
                gitignore_file.write(gitignore_content)
            print(f"{gitignore_path} ファイルが作成され、内容が書き込まれました。")
        except Exception as e:
            print(f"エラー: {e}")
            
    @staticmethod
    def create_env():
        env_path = '.env'

        # .env ファイルの内容
        env_content = [
            "LINE_NOTIFY_TOKEN=",
            "DATABASE_URL=your_database_url",
            "API_KEY=your_api_key"
        ]

        # 既に .env ファイルが存在する場合は処理を停止
        if os.path.exists(env_path):
            print(f"{env_path} ファイルは既に存在しています。処理を停止します。")
            return

        try:
            # .env ファイルを作成し、内容を書き込む
            with open(env_path, 'w') as env_file:
                # 最初の行だけ入力を促す
                first_line = env_content[0]
                user_input = input(f"Enter value for {first_line.split('=')[0]}: ")
                env_file.write(f"{first_line}{user_input}\n")

                # 残りの行は元の内容を書き込む
                for line in env_content[1:]:
                    env_file.write(f"{line}\n")

            print(f"{env_path} ファイルが作成され、内容が書き込まれました。")
        except Exception as e:
            print(f"エラー: {e}")

    @staticmethod
    def firstsetup():
        # 関数を呼び出して .gitignore ファイルを作成
        sapnet.create_gitignore()
        sapnet.create_env()
        
    @staticmethod
    # 拡散する先をソートして返します。
    def next_Allpair(df,stimulus):#sapnetモジュール内で使用
        sapnet.logger.debug("(2/10)Calculating next_Allpair")
        diffusion_list = []
        column = df.iloc[:, stimulus]
        for i in range(len(column)):
            distance_value = column[i]
            if distance_value > 0:# 距離を持たないものを飛ばす（つながってないもの）
                if stimulus == i+1: # 刺激値とi+1が同じ（活性値を保持する部分）は飛ばす
                    continue
                #print(stimulus,i+1)
                diffusion_list.append([distance_value,stimulus,i+1])
                # 配列を一番前の少数を基準にソート
                sorted_diffusion_list = sorted(diffusion_list, key=lambda x: x[0])
                #print(sorted_diffusion_list)
                # 今回の拡散が行われるリスト
                pair_list = [sublist[1:] for sublist in sorted_diffusion_list]
                #print(pair_list)
                # 次のパス一覧を返却
                path_list = [sublist[1:] for sublist in pair_list]
                next_list = [[sublist[0] for sublist in path_list]]
        sapnet.logger.debug("(2/10)Calculating next_Allpair %s",pair_list)
        return pair_list


    @staticmethod
    def already_pair_remove(pair_list,already_list):#sapnetモジュール内で使用
        return_list = []
        for pair_temp in pair_list:
            if pair_temp not in already_list:
                return_list.append(pair_temp)
                already_list.append(pair_temp)
                reversed_pair = pair_temp[::-1]
                already_list.append(reversed_pair)
                sapnet.logger.debug("(3/10)Removing already pairs %s  %s",pair_temp,reversed_pair)
            else:
                None
        return return_list,already_list


    @staticmethod
    def path_count(df, stimulus):
        sapnet.logger.debug("(5/10)Counting paths for stimulus  %s", stimulus)
        column_name = df.columns[stimulus]  # 指定された数値から列名を取得
        selected_row = df.iloc[stimulus - 1]  # 指定された行を選択
        # print(column_name)
        # print(selected_row)
        # 行の名前と同じ行の数値以外を取得
        row_values = selected_row.drop(index=column_name)
        # print(row_values)
        # 0.0より大きい数値のカウントを追加
        count_above_0 = 0
        for value in row_values[1:]:
            if value > 0.0:
                count_above_0 += 1
        # print("0.0より大きい数値の個数:", count_above_0)
        sapnet.logger.debug("(5/10)Counting paths for stimulus %s --> %s",stimulus,count_above_0)

        return count_above_0


    @staticmethod
    def path_weight(df, stimulus,receive):
        sapnet.logger.debug("(6/10)Calculating path weight for stimulus %s and receive %s", stimulus,receive)
        row_number = stimulus-1# 例として2を指定
        column_number = receive
        if stimulus != receive:
            weight = df.iloc[row_number,column_number]
            sapnet.logger.debug("(6/10)Calculating path weight for stimulus %s -> %s --> %s",stimulus,receive,weight)
            return weight


    @staticmethod
    #データフレームを渡すとsapnetのアルゴリズムに基づいてペアとなるリストを返します。
    def stimulus_pairlist(df,stimulus):
        sapnet.logger.info("(1/10)Generating stimulus pair list for stimulus %s", stimulus)
        already_list=[]
        temp_list = [stimulus]
        path_num_list = []
        path_weight_list = []
        return_pairlist = []
        #print("temp",temp_list)
        while len(temp_list)!=0:
            #print(i)
            now_list = temp_list
            temp_list = []
            for item in range(len(now_list)):
                #print("item",now_list[item])
                pair_list = sapnet.next_Allpair(df,now_list[item])
                #print("pair",pair_list)
                check_pair_list,already_list = sapnet.already_pair_remove(pair_list,already_list)
                #print("al",already_list)
                #print("check",check_pair_list)
                path_list = [sublist[1:] for sublist in check_pair_list]
                next_list = [sublist[0] for sublist in path_list]
                # print("next",next_list)
                temp_list.extend(next_list)
                # print("check",temp_list)
                for active_pair in check_pair_list:
                    ## print(active_pair)
                    return_pairlist.append(active_pair)
                    # 計算部分
                    # offer_num,receive_num = active_pair[0],active_pair[1]
                    # N = sapnet.path_num_calc(df,offer_num)
                    # path_num_list.append(N)
                    # #print(N)
                    # w = sapnet.path_weight_calc(df,offer_num,receive_num)
                    # path_weight_list.append(w)
                    # #print(w)
        sapnet.logger.info("(3/10)Generating stimulus pair list: %s", return_pairlist)
        return return_pairlist


    @staticmethod
    def stimulus_add_value(path_quantity,path_weight,last_list,pairA,pairB):
        sapnet.logger.debug("(7/10)calculation stimulus value for pairA( %s )and pairB( %s )",pairA,pairB)
        sapnet.logger.debug("(7/10)Lastlist before update: %s", last_list)  # 更新前のラストリストを表示
        last_value = last_list[pairA-1]
        sapnet.logger.debug("(7/10)pickup last value pair( %s ):",pairA, last_value)  # 更新前のラストリストを表示
        N = path_quantity
        w = path_weight
        v = (1/N)*last_value*math.exp(-w)
        sapnet.logger.debug("(7/10)Calculation -> 1/ %s * %s * exp(- %s )",N,last_value,w)
        sapnet.logger.debug("(7/10)Calculation -> %s",v)
        last_list[pairB-1] = v
        sapnet.logger.debug("(7/10)Lastlist after update: %s", last_list)  # 更新後のラストリストを表示
        return v,last_list


    @staticmethod
    def last_dataframe_setting(df,stimulus,first_stimulus_value):
        # 元のデータフレームの長さを取得
        length = len(df)
        last_list=[]
        # 0の列を指定された数だけ追加
        for i in range(length):
            if i == stimulus-1:
                last_list.append(first_stimulus_value)  # 新しい列を追加し、指定された列に1を設定
                df.iloc[i, i+1] += first_stimulus_value
            else:
                last_list.append(0)  # それ以外の列は0を設定
        sapnet.logger.debug("(4/10)Creating last dataframe for stimulus %s ->",stimulus,last_list)
        return last_list


    @staticmethod
    def df_update(df,stimulus_value,pairA,pairB):
        sapnet.logger.debug("(9/10)Updating DataFrame")  # デバッグ情報：データフレームの更新開始
        # 数値で行と列を指定して値に1を加算
        row_index = pairB  # 行のインデックス (0から始まる)
        col_index = pairB  # 列のインデックス (0から始まる)
        sapnet.logger.debug("(9/10)moved from %s to %s adding %s.",pairA,pairB,stimulus_value)
        df.iloc[row_index-1, col_index] += stimulus_value
        sapnet.logger.debug("(9/10)DataFrame update completed")  # デバッグ情報：データフレームの更新が完了

        return df


    @staticmethod
    def create_graph(df,GIF_source_path,plotpoint_list):
        diagonal_matrix = np.diag(df.iloc[:, 1:].values)
        plotpoint_list.append(diagonal_matrix)
        plt.bar(np.arange(len(diagonal_matrix)) + 1, diagonal_matrix, color='b')
        plt.title('Stimulus_value')
        plt.xlabel('Knowledge')
        plt.ylabel('Values')
        # 指定したフォルダ内のファイルをリスト
        files = os.listdir(GIF_source_path)
        # PNGファイルの数をカウント
        png_count = sum(1 for file in files if file.lower().endswith(".png"))
        # フォーマットされたファイル名を生成
        image_filename = os.path.join(GIF_source_path, f"gif_source_{png_count+1:03d}")

        if GIF_source_path:
            plt.savefig(image_filename)
            plt.close()
        else:
            plt.show()
        sapnet.logger.debug("(8/10)Make DataFrame graph")  # デバッグ情報：データフレームの更新が完了
        return plotpoint_list


    @staticmethod
    def create_gif(GIF_source_path, GIF_100_path,GIF_1000_path):
        # GIF用の画像ファイルリストを取得
        image_list = sorted([os.path.join(GIF_source_path, file) for file in os.listdir(GIF_source_path) if file.lower().endswith(".png")])
        # 画像リストが存在しない場合は処理を中止
        if not image_list:
            sapnet.logger.debug("(10/10)No image files found in the source path.")
            return
        # 画像を開いてリストに格納
        images = [Image.open(img) for img in image_list]
        # GIFファイルを生成
        images[0].save(GIF_100_path, save_all=True, append_images=images[1:], duration=100, loop=0)
        images[0].save(GIF_1000_path, save_all=True, append_images=images[1:], duration=1000, loop=0)
        sapnet.logger.debug("(10/10)Make Gif image completed")  # デバッグ情報：データフレームの更新が完了


    @staticmethod
    def attenuation(df,attenuation_percentage):#減衰関数
        # 少数で指定された数値分削る関数
        # 元のデータフレームの長さを取得
        length = len(df)
        # 0の列を指定された数だけ追加
        for i in range(length):
            df.iloc[i, i+1] *= (1-attenuation_percentage)
        return df


    @staticmethod
    def makeup_folder():
        # 現在時刻を取得
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 現在時刻を使用することでアウトプットファルダを重複なく作成することができる
        folder_name = f"./Output_{current_time}"
        # if not os.path.exists(folder_name):
        #     os.makedirs(folder_name)
        # 現在時刻を使用することでアウトプットファルダを重複なく作成することができる
        gif_folder_name = folder_name+"/GIF_source/"
        if not os.path.exists(gif_folder_name):
            os.makedirs(gif_folder_name)
        Heatmap_path = folder_name + '/heatmap.png'
        Network_path = folder_name + '/network.png'
        Plotpoint_path = folder_name + '/plotpoint.png'
        GIF_source_path = gif_folder_name
        GIF_100_path = folder_name + '/graph_100.gif'
        GIF_1000_path = folder_name + '/graph_1000.gif'

        return folder_name,Heatmap_path,Network_path,Plotpoint_path,GIF_source_path,GIF_100_path,GIF_1000_path


    @staticmethod
    def create_heatmap(df,Heatmap_path):
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.set_index('name'), annot=True, cmap='winter', linewidths=.5)
        plt.title("既存知識の類似度ヒートマップ")
        plt.savefig(Heatmap_path)
        plt.close()


    @staticmethod
    def create_network(df,Network_path):
        df_reset = df.set_index('name')
        # 空の有向グラフを作成
        G = nx.DiGraph()
        # ノードを追加
        for node in df_reset.index:
            G.add_node(node, size=df_reset.loc[node, node])
        # エッジを追加
        for source in df_reset.index:
            for target in df_reset.columns:
                if source != target:
                    # 対角行列の値をノードの値とし、それ以外をエッジの値とする
                    edge_value = df_reset.loc[source, target]
                    if edge_value > 0.0:
                        # 0.0でない場合のみエッジを追加
                        G.add_edge(source, target, weight=edge_value)
        # ネットワークを可視化
        pos = nx.spring_layout(G)  # レイアウト設定
        node_sizes = [G.nodes[node]['size'] * 5000 for node in G.nodes]  # ノードのサイズを設定
        # エッジの太さを逆にする
        edge_widths = [1 / G.edges[edge]['weight'] * 1.5 for edge in G.edges]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)
        nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='gray', alpha=0.7)
        nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')
        edge_labels = {(source, target): f"{G.edges[(source, target)]['weight']:.1f}" for source, target in G.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        plt.title("既存知識の類似度ネットワーク")
        # グラフを出力
        plt.savefig(Network_path)
        plt.close()


    @staticmethod
    def create_plotpoint(plotpoint_list, plotpoint_path):
        # 実際にプロットしたいデータ
        transposed_plotpoint_list = [list(row) for row in zip(*plotpoint_list)]

        plt.figure(figsize=(10, 6))  # グラフ全体のサイズを設定
        sapnet.logger.debug("The data list is as follows: %s",transposed_plotpoint_list)

        # 各データ列に対して折れ線グラフをプロット
        for data_list in transposed_plotpoint_list:
            name = data_list[0]
            data = data_list[1:]
            plt.plot(range(len(data)), data, marker='o', label=name)

        plt.title('活性値の推移 (減衰なし)')  # グラフのタイトル
        plt.xlabel('count')  # X軸のラベル
        plt.ylabel('活性値')  # Y軸のラベル
        plt.ylim(0, 1.0)  # Y軸の上限値を調整
        plt.legend()  # 凡例を表示

        # x軸のラベルを1毎に表示
        x_values = list(range(len(data)))
        plt.xticks(x_values, x_values)
        plt.savefig(plotpoint_path)
        plt.close()

    @staticmethod
    def send_line_notify(notification_message):
        # 環境変数を読み込む
        line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')        
        #LINEに通知する
        if line_notify_token is None:
            print("LINE_NOTIFY_TOKENが設定されていません。")
            return
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': f'\n{notification_message}'}
        requests.post(line_notify_api, headers = headers, data = data)

    @staticmethod
    def knowledge_selection(df):
        diagonal_matrix = np.diag(df.iloc[:, 1:].values)
        # 1未満の要素を含めずに新しい配列を作成
        valid_elements = diagonal_matrix[diagonal_matrix >= 1]
        # ソフトマックス関数を適用
        exp_values = np.exp(valid_elements - np.max(valid_elements))
        softmax_values = exp_values / np.sum(exp_values)
        # np.random.choiceを使用してランダムに選択
        selected_index = np.random.choice(len(valid_elements), p=softmax_values)
        # 元のリストの中でのインデックスを取得
        original_index = np.where(diagonal_matrix >= 1)[0][selected_index]
        return original_index
    
    def count_elements(lst):
        max_element = max(lst)  # リスト内の最大値を取得
        element_count = [0] * (max_element + 1)  # 要素番号0から最大値までの出現回数を格納するリストを初期化
        for element in lst:
            element_count[element] += 1
        return element_count

    def create_selection_graph(data):
        # データ
        labels = list(range(len(data)))  # データの数に対応するラベルを0から順に生成

        # 棒グラフの描画
        plt.bar(labels, data)

        # グラフにタイトルやラベルを追加
        plt.title('Bar Chart')
        plt.xlabel('Category')
        plt.ylabel('Value')

        # x軸のラベルを設定
        plt.xticks(labels)

        # グラフを表示
        plt.show()

    

    @staticmethod
    def stimulus_calc(df=None, stimulus=1, first_stimulus_value=1.0, debug=0, graph=0):
        if debug==0:
            logging.getLogger(__name__).setLevel(logging.CRITICAL)
        if debug==1:
            logging.getLogger(__name__).setLevel(logging.INFO)
        if debug==2:
            logging.getLogger(__name__).setLevel(logging.DEBUG)
        if df is None:
            df = sapnet.example_dataframe()
        sapnet.logger.info("Sapnet's algorithm, Start the calculations.")
        pair_list = sapnet.stimulus_pairlist(df,stimulus)
        last_list = sapnet.last_dataframe_setting(df,stimulus,first_stimulus_value)
        if graph == 1:
            folder_name,Heatmap_path,Network_path,Plotpoint_path,GIF_source_path,GIF_100_path,GIF_1000_path = sapnet.makeup_folder()
            sapnet.create_heatmap(df,Heatmap_path)
            plotpoint_list = [list(df['name'])]

        for pair in pair_list:
            paths = sapnet.path_count(df,pair[0])
            weight = sapnet.path_weight(df,pair[0],pair[1])
            stimulus_value,last_list = sapnet.stimulus_add_value(paths,weight,last_list,pair[0],pair[1])
            if graph == 1:
                plotpoint_list=sapnet.create_graph(df,GIF_source_path,plotpoint_list)
            df = sapnet.df_update(df,stimulus_value,pair[0],pair[1])
        
        if graph == 1:
            plotpoint_list=sapnet.create_graph(df,GIF_source_path,plotpoint_list)
            sapnet.create_plotpoint(plotpoint_list,Plotpoint_path)
            sapnet.create_network(df,Network_path)
            sapnet.create_gif(GIF_source_path,GIF_100_path,GIF_1000_path)
        return df