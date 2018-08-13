import pytest
import os
import configparser
import sqlite3

def test_run_sim():

    from infSim.sim import run_sim
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    ## DUMMY DATA ##

    dummy_nodes = list()
    dummy_nodes.append((1,0,1,1))
    dummy_nodes.append((2,2,1,0))
    dummy_nodes.append((3,0,1,1))
    dummy_nodes.append((4,3,1,0))
    dummy_nodes.append((5,2,1,0))
    dummy_nodes.append((6,2,1,0))


    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,4))
    dummy_edges.append((1,5))
    dummy_edges.append((2,1))
    dummy_edges.append((2,3))
    dummy_edges.append((2,4))
    dummy_edges.append((2,6))
    dummy_edges.append((3,2))
    dummy_edges.append((3,4))
    dummy_edges.append((4,1))
    dummy_edges.append((4,2))
    dummy_edges.append((4,3))
    dummy_edges.append((5,1))
    dummy_edges.append((5,6))
    dummy_edges.append((6,2))
    dummy_edges.append((6,5))

    dummy_active = list()
    dummy_active.append((1,0,1))
    dummy_active.append((3,0,1))

    ## TEST SETUP - Lambda One ##
    directory_name = os.getcwd()
    
    params = dict(lambda_val=1)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Be Influenced')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Be Influenced')
        
        if node['nodeID'] == 4:

            pytest.fail('Node 4 Should Only Be Influenced When Lambda > 1')
        
        influenced_count += 1
    
    assert influenced_count == 3
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Have Been Activated')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Have Been Activated')
        
        if node['nodeID'] == 4:

            pytest.fail('Node 4 Should Only Be Activated When Lambda > 1')
        
        if node['nodeID'] == 1:

            if node['round'] != 0:

                pytest.fail('Node 1 Should Only Be Active First Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 0:

                pytest.fail('Node 3 Should Only Be Active First Round')        

        if node['nodeID'] == 2:

            if node['round'] != 1:

                pytest.fail('Node 2 Should Only Be Active Second Round')
        
        active_count += 1
    
    assert active_count == 3

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')

    ## TEST SETUP - Lambda Two ##
    directory_name = os.getcwd()
    
    params = dict(lambda_val=2)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row

    dummy_nodes = list()
    dummy_nodes.append((1,0,2,1))
    dummy_nodes.append((2,2,2,0))
    dummy_nodes.append((3,0,2,1))
    dummy_nodes.append((4,3,2,0))
    dummy_nodes.append((5,2,2,0))
    dummy_nodes.append((6,2,2,0))
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Be Influenced')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Be Influenced')
        
        influenced_count += 1
    
    assert influenced_count == 4
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Have Been Activated')
        
        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Have Been Activated')
        
        if node['nodeID'] == 4:

            if node['round'] != 2 and node['round'] !=3:

                pytest.fail('Node 4 Should Only Be Activated Third and Fourth Round')
        
        if node['nodeID'] == 1:

            if node['round'] != 0 and node['round'] != 1:

                pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 0 and node['round'] != 1:

                pytest.fail('Node 3 Should Only Be Active First and Second Round')        

        if node['nodeID'] == 2:

            if node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')
        
        active_count += 1
    
    assert active_count == 8

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('simulation-details.csv')

# def test_run_sim_decay_one():

#     from infSim.sim import run_sim
#     from infSim.settings import make_settings_file
#     from infSim.db import create_db

#     '''
#     In this test the dummy data from lambda two test above has an additional node which will allow node 4 to still become activated. 
#     '''
    
#     ## DUMMY DATA ##

#     dummy_nodes = list()
#     dummy_nodes.append((1,0,2,1))
#     dummy_nodes.append((2,2,2,0))
#     dummy_nodes.append((3,0,2,1))
#     dummy_nodes.append((4,3,2,0))
#     dummy_nodes.append((5,2,2,0))
#     dummy_nodes.append((6,2,2,0))
#     dummy_nodes.append((7,2,2,0))


#     dummy_edges = list()
#     dummy_edges.append((1,2))
#     dummy_edges.append((1,4))
#     dummy_edges.append((1,5))
#     dummy_edges.append((1,7))
#     dummy_edges.append((2,1))
#     dummy_edges.append((2,3))
#     dummy_edges.append((2,4))
#     dummy_edges.append((2,6))
#     dummy_edges.append((3,2))
#     dummy_edges.append((3,4))
#     dummy_edges.append((3,7))
#     dummy_edges.append((4,1))
#     dummy_edges.append((4,2))
#     dummy_edges.append((4,3))
#     dummy_edges.append((4,7))
#     dummy_edges.append((5,1))
#     dummy_edges.append((5,6))
#     dummy_edges.append((6,2))
#     dummy_edges.append((6,5))
#     dummy_edges.append((7,1))
#     dummy_edges.append((7,3))
#     dummy_edges.append((7,4))

#     dummy_active = list()
#     dummy_active.append((1,0,1))
#     dummy_active.append((3,0,1))

#     directory_name = os.getcwd()
    
#     params = dict(lambda_val=2,decay=1)
#     make_settings_file(directory_name, directory_name, params)

#     config = configparser.ConfigParser()
#     config.read(directory_name + '/settings.ini')
#     conn = sqlite3.connect(config['FILES']['DB'])
#     conn.row_factory = sqlite3.Row
    
#     create_db(conn)

#     conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
#     conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
#     conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

#     conn.commit()

#     run_sim(config, conn)

#     influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

#     influenced_count = 0
#     for node in influenced_nodes:

#         if node['nodeID'] == 5:

#             pytest.fail('Node 5 Should Not Be Influenced')
        
#         if node['nodeID'] == 6:

#             pytest.fail('Node 6 Should Not Be Influenced')
        
#         influenced_count += 1
    
#     assert influenced_count == 5
    
#     active_nodes = conn.execute('SELECT * FROM activeNodes')

#     active_count=0
#     for node in active_nodes:

#         if node['nodeID'] == 5:

#             pytest.fail('Node 5 Should Not Have Been Activated')
        
#         if node['nodeID'] == 6:

#             pytest.fail('Node 6 Should Not Have Been Activated')
        
#         if node['nodeID'] == 4:

#             if node['round'] != 2 and node['round'] !=3:

#                 pytest.fail('Node 4 Should Only Be Activated Third and Fourth Round')
        
#         if node['nodeID'] == 1:

#             if node['round'] != 0 and node['round'] != 1:

#                 pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
#         if node['nodeID'] == 3:

#             if node['round'] != 0 and node['round'] != 1:

#                 pytest.fail('Node 3 Should Only Be Active First and Second Round')        

#         if node['nodeID'] == 2:

#             if node['round'] != 1 and node['round'] != 2:

#                 pytest.fail('Node 2 Should Only Be Active Second and Third Round')

#         if node['nodeID'] == 7:

#             if node['round'] != 1 and node['round'] != 2:

#                 pytest.fail('Node 7 Should Only Be Active Second and Third Round')
        
#         active_count += 1
    
#     assert active_count == 10

#     conn.close()
#     os.remove(config['FILES']['DB'])
#     os.remove('settings.ini')
#     os.remove('simulation-details.csv')

# def test_run_sim_decay_two():

#     from infSim.sim import run_sim
#     from infSim.settings import make_settings_file
#     from infSim.db import create_db

#     '''
#     In this test the dummy data from lambda two test above is the same as above and now node 4 will not meet the threshold value because of decay on 1 and 3. 
#     '''
    
#     ## DUMMY DATA ##

#     dummy_nodes = list()
#     dummy_nodes.append((1,0,2,1))
#     dummy_nodes.append((2,2,2,0))
#     dummy_nodes.append((3,0,2,1))
#     dummy_nodes.append((4,3,2,0))
#     dummy_nodes.append((5,2,2,0))
#     dummy_nodes.append((6,2,2,0))


#     dummy_edges = list()
#     dummy_edges.append((1,2))
#     dummy_edges.append((1,4))
#     dummy_edges.append((1,5))
#     dummy_edges.append((2,1))
#     dummy_edges.append((2,3))
#     dummy_edges.append((2,4))
#     dummy_edges.append((2,6))
#     dummy_edges.append((3,2))
#     dummy_edges.append((3,4))
#     dummy_edges.append((4,1))
#     dummy_edges.append((4,2))
#     dummy_edges.append((4,3))
#     dummy_edges.append((5,1))
#     dummy_edges.append((5,6))
#     dummy_edges.append((6,2))
#     dummy_edges.append((6,5))

#     dummy_active = list()
#     dummy_active.append((1,0,1))
#     dummy_active.append((3,0,1))

#     directory_name = os.getcwd()
    
#     params = dict(lambda_val=2, decay=1)
#     make_settings_file(directory_name, directory_name, params)

#     config = configparser.ConfigParser()
#     config.read(directory_name + '/settings.ini')
#     conn = sqlite3.connect(config['FILES']['DB'])
#     conn.row_factory = sqlite3.Row
    
#     create_db(conn)

#     conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
#     conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
#     conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

#     conn.commit()

#     run_sim(config, conn)

#     influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

#     influenced_count = 0
#     for node in influenced_nodes:

#         if node['nodeID'] == 5:

#             pytest.fail('Node 5 Should Not Be Influenced')
        
#         if node['nodeID'] == 6:

#             pytest.fail('Node 6 Should Not Be Influenced')
        
#         if node['nodeID'] == 4:

#             pytest.fail('Node 4 Should Not Be Influenced due to the decay')
        
#         influenced_count += 1
    
#     assert influenced_count == 3
    
#     active_nodes = conn.execute('SELECT * FROM activeNodes')

#     active_count=0
#     for node in active_nodes:

#         if node['nodeID'] == 5:

#             pytest.fail('Node 5 Should Not Have Been Activated')
        
#         if node['nodeID'] == 6:

#             pytest.fail('Node 6 Should Not Have Been Activated')
        
#         if node['nodeID'] == 4:

#             pytest.fail('Node 4 Should Not Have Been Activated')
        
#         if node['nodeID'] == 1:

#             if node['round'] != 0 and node['round'] != 1:

#                 pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
#         if node['nodeID'] == 3:

#             if node['round'] != 0 and node['round'] != 1:

#                 pytest.fail('Node 3 Should Only Be Active First and Second Round')        

#         if node['nodeID'] == 2:

#             if node['round'] != 1 and node['round'] != 2:

#                 pytest.fail('Node 2 Should Only Be Active Second and Third Round')
        
#         active_count += 1
    
#     assert active_count == 6

#     conn.close()
#     os.remove(config['FILES']['DB'])
#     os.remove('settings.ini')
#     os.remove('simulation-details.csv')

def test_run_sim_lambda_3():

    from infSim.sim import run_sim
    from infSim.settings import make_settings_file
    from infSim.db import create_db
    from infSim.initiate import lambda_value_degree

   
    ## DUMMY DATA ##

    dummy_nodes = list()
    dummy_nodes.append((1,0,3,1))
    dummy_nodes.append((2,4,3,0))
    dummy_nodes.append((3,1,3,0))
    dummy_nodes.append((4,1,3,0))
    dummy_nodes.append((5,1,3,0))
    dummy_nodes.append((6,2,3,0))
    dummy_nodes.append((7,1,3,0))
    dummy_nodes.append((8,2,3,0))



    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,3))
    dummy_edges.append((1,7))
    dummy_edges.append((1,8))
    dummy_edges.append((2,1))
    dummy_edges.append((2,3))
    dummy_edges.append((2,4))
    dummy_edges.append((2,5))
    dummy_edges.append((2,8))
    dummy_edges.append((3,1))
    dummy_edges.append((3,2))
    dummy_edges.append((3,4))
    dummy_edges.append((4,2))
    dummy_edges.append((4,3))
    dummy_edges.append((4,5))
    dummy_edges.append((4,6))
    dummy_edges.append((5,4))
    dummy_edges.append((5,2))
    dummy_edges.append((6,4))
    dummy_edges.append((6,7))
    dummy_edges.append((7,1))
    dummy_edges.append((7,6))
    dummy_edges.append((8,1))
    dummy_edges.append((8,2))

    dummy_active = list()
    dummy_active.append((1,0,1))

    directory_name = os.getcwd()
    
    params = dict(lambda_val=2,decay=0)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 2:

            pytest.fail('Node 2 Should Not Be Influenced')
        
        if node['nodeID'] == 8:

            pytest.fail('Node 8 Should Not Be Influenced')
        
        influenced_count += 1
    
    assert influenced_count == 6
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 2:

            pytest.fail('Node 2 Should Not Have Been Activated')
        
        if node['nodeID'] == 8:

            pytest.fail('Node 8 Should Not Have Been Activated')
        
        if node['nodeID'] == 4:

            if node['round'] != 2 and node['round'] !=3 and node['round'] != 4:

                pytest.fail('Node 4 Should Only Be Activated Third, Fourth, Fifth Round')
        
        if node['nodeID'] == 1:

            if node['round'] != 0 and node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 1 Should Only Be Active First, Second, Third Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 1 and node['round'] != 2 and node['round'] != 3:

                pytest.fail('Node 3 Should Only Be Active Second, Third, Fourth Round')        

        if node['nodeID'] == 6:

            if node['round'] != 3 and node['round'] != 4 and node['round'] != 5:

                pytest.fail('Node 2 Should Only Be Active Rounds 4, 5, 6')

        if node['nodeID'] == 7:

            if node['round'] != 1 and node['round'] != 2 and node['round'] != 3:

                pytest.fail('Node 7 Should Only Be Active Second, Third, Fourth Rounds') 

        if node['nodeID'] == 5:

            if node['round'] != 3 and node['round'] != 4 and node['round'] != 5:

                pytest.fail('Node 5 Should Only Be Active Second, Third, Fourth Round')      
        
        active_count += 1
    
    assert active_count == 16 # There is no round 6

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('simulation-details.csv')

def test_run_sim_lambda_degree():

    from infSim.sim import run_sim
    from infSim.settings import make_settings_file
    from infSim.db import create_db
    from infSim.initiate import lambda_value_degree

   
    ## DUMMY DATA ##

    dummy_nodes = list()
    dummy_nodes.append((1,0,4,1))
    dummy_nodes.append((2,4,5,0))
    dummy_nodes.append((3,1,3,0))
    dummy_nodes.append((4,1,2,0))
    dummy_nodes.append((5,1,3,0))
    dummy_nodes.append((6,2,2,0))
    dummy_nodes.append((7,1,2,0))
    dummy_nodes.append((8,2,2,0))

    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,3))
    dummy_edges.append((1,7))
    dummy_edges.append((1,8))
    dummy_edges.append((2,1))
    dummy_edges.append((2,3))
    dummy_edges.append((2,4))
    dummy_edges.append((2,5))
    dummy_edges.append((2,8))
    dummy_edges.append((3,1))
    dummy_edges.append((3,2))
    dummy_edges.append((3,4))
    dummy_edges.append((4,2))
    dummy_edges.append((4,3))
    dummy_edges.append((4,5))
    dummy_edges.append((5,2))
    dummy_edges.append((5,4))
    dummy_edges.append((5,6))
    dummy_edges.append((6,5))
    dummy_edges.append((6,7))
    dummy_edges.append((7,1))
    dummy_edges.append((7,6))
    dummy_edges.append((8,1))
    dummy_edges.append((8,2))

    dummy_active = list()
    dummy_active.append((1,0,1))

    directory_name = os.getcwd()
    
    params = dict(lambda_val=2,decay=0)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Be Influenced')
        
        if node['nodeID'] == 8:

            pytest.fail('Node 8 Should Not Be Influenced')
        
        influenced_count += 1
    
    assert influenced_count == 6
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 6:

            pytest.fail('Node 6 Should Not Have Been Activated')
        
        if node['nodeID'] == 8:

            pytest.fail('Node 8 Should Not Have Been Activated')
        
        if node['nodeID'] == 4:

            if node['round'] != 2 and node['round'] !=3:

                pytest.fail('Node 4 Should Only Be Activated Third, Fourth Rounds')
        
        if node['nodeID'] == 1:

            if node['round'] != 0 and node['round'] != 1 and node['round'] != 2 and node['round'] != 3:

                pytest.fail('Node 1 Should Only Be Active First, Second, Third, Fourth Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 1 and node['round'] != 2 and node['round'] != 3:

                pytest.fail('Node 3 Should Only Be Active Second, Third, Fourth Round')        

        if node['nodeID'] == 2:

            if node['round'] != 4 and node['round'] != 5:

                pytest.fail('Node 2 Should Only Be Active Rounds 5, 6')

        if node['nodeID'] == 7:

            if node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 7 Should Only Be Active Second, Third Rounds')   
        
        if node['nodeID'] == 5:

            if node['round'] != 3 and node['round'] != 4 and node['round'] != 5:

                pytest.fail('Node 5 Should Only Be Active Second, Third, Fourth Round')  
                 
        active_count += 1
    
    assert active_count == 16 # There is no round 6

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('simulation-details.csv')


# def test_run_sim_decay_one():

#     from infSim.sim import run_sim
#     from infSim.settings import make_settings_file
#     from infSim.db import create_db

#     '''
#     In this test the dummy data from lambda two test above has an additional node which will allow node 4 to still become activated. 
#     '''
    
#     ## DUMMY DATA ##

#     dummy_nodes = list()
#     dummy_nodes.append((1,0,2,1))
#     dummy_nodes.append((2,2,2,0))
#     dummy_nodes.append((3,0,2,1))
#     dummy_nodes.append((4,3,2,0))
#     dummy_nodes.append((5,2,2,0))
#     dummy_nodes.append((6,2,2,0))
#     dummy_nodes.append((7,2,2,0))


#     dummy_edges = list()
#     dummy_edges.append((1,2))
#     dummy_edges.append((1,4))
#     dummy_edges.append((1,5))
#     dummy_edges.append((1,7))
#     dummy_edges.append((2,1))
#     dummy_edges.append((2,3))
#     dummy_edges.append((2,4))
#     dummy_edges.append((2,6))
#     dummy_edges.append((3,2))
#     dummy_edges.append((3,4))
#     dummy_edges.append((3,7))
#     dummy_edges.append((4,1))
#     dummy_edges.append((4,2))
#     dummy_edges.append((4,3))
#     dummy_edges.append((4,7))
#     dummy_edges.append((5,1))
#     dummy_edges.append((5,6))
#     dummy_edges.append((6,2))
#     dummy_edges.append((6,5))
#     dummy_edges.append((7,1))
#     dummy_edges.append((7,3))
#     dummy_edges.append((7,4))

#     dummy_active = list()
#     dummy_active.append((1,0,1))
#     dummy_active.append((3,0,1))

#     directory_name = os.getcwd()
    
#     params = dict(lambda_val=2,decay=1)
#     make_settings_file(directory_name, directory_name, params)

#     config = configparser.ConfigParser()
#     config.read(directory_name + '/settings.ini')
#     conn = sqlite3.connect(config['FILES']['DB'])
#     conn.row_factory = sqlite3.Row
    
#     create_db(conn)

#     conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
#     conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
#     conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

#     conn.commit()

#     run_sim(config, conn)

#     influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

#     influenced_count = 0
#     for node in influenced_nodes:

#         if node['nodeID'] == 5:

#             pytest.fail('Node 5 Should Not Be Influenced')
        
#         if node['nodeID'] == 6:

#             pytest.fail('Node 6 Should Not Be Influenced')
        
#         influenced_count += 1
    
#     assert influenced_count == 5
    
#     active_nodes = conn.execute('SELECT * FROM activeNodes')

#     active_count=0
#     for node in active_nodes:

#         if node['nodeID'] == 5:

#             pytest.fail('Node 5 Should Not Have Been Activated')
        
#         if node['nodeID'] == 6:

#             pytest.fail('Node 6 Should Not Have Been Activated')
        
#         if node['nodeID'] == 4:

#             if node['round'] != 2 and node['round'] !=3:

#                 pytest.fail('Node 4 Should Only Be Activated Third and Fourth Round')
        
#         if node['nodeID'] == 1:

#             if node['round'] != 0 and node['round'] != 1:

#                 pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
#         if node['nodeID'] == 3:

#             if node['round'] != 0 and node['round'] != 1:

#                 pytest.fail('Node 3 Should Only Be Active First and Second Round')        

#         if node['nodeID'] == 2:

#             if node['round'] != 1 and node['round'] != 2:

#                 pytest.fail('Node 2 Should Only Be Active Second and Third Round')

#         if node['nodeID'] == 7:

#             if node['round'] != 1 and node['round'] != 2:

#                 pytest.fail('Node 7 Should Only Be Active Second and Third Round')
        
#         active_count += 1
    
#     assert active_count == 10

#     conn.close()
#     os.remove(config['FILES']['DB'])
#     os.remove('settings.ini')
#     os.remove('simulation-details.csv')


def test_run_sim_decay_lambda_2():

    from infSim.sim import run_sim
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    '''
    In this test the dummy data from lambda two test above is the same as above and now node 4 will not meet the threshold value because of decay on 1 and 3. 
    '''
    
    ## DUMMY DATA ##

    dummy_nodes = list()
    dummy_nodes.append((1,0,2,1))
    dummy_nodes.append((2,2,2,0))
    dummy_nodes.append((3,2,2,0))
    dummy_nodes.append((4,7,2,0))
    dummy_nodes.append((5,5,2,0))
    dummy_nodes.append((6,1,2,0))
    dummy_nodes.append((7,1,2,0))


    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,3))
    dummy_edges.append((1,4))
    dummy_edges.append((2,1))
    dummy_edges.append((2,4))
    dummy_edges.append((2,6))
    dummy_edges.append((3,1))
    dummy_edges.append((3,4))
    dummy_edges.append((4,1))
    dummy_edges.append((4,2))
    dummy_edges.append((4,3))
    dummy_edges.append((4,5))
    dummy_edges.append((5,4))
    dummy_edges.append((6,2))
    dummy_edges.append((6,7))
    dummy_edges.append((7,6))

    dummy_active = list()
    dummy_active.append((1,0,3))

    directory_name = os.getcwd()
    
    params = dict(lambda_val=2, decay=1)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:

        if node['nodeID'] == 4:

            pytest.fail('Node 4 Should Not Be Influenced')
        
        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Be Influenced')
        
        influenced_count += 1
    
    assert influenced_count == 5
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 4:

            pytest.fail('Node 4 Should Not Have Been Activated')
        
        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Have Been Activated')
        
        if node['nodeID'] == 1:

            if node['round'] != 0 and node['round'] != 1:

                pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 3 Should Only Be Active Second and Third Round')        

        if node['nodeID'] == 2:

            if node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')

        if node['nodeID'] == 6:

            if node['round'] != 2 and node['round'] != 3:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')

        if node['nodeID'] == 7:

            if node['round'] != 3 and node['round'] != 4:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')
        
        active_count += 1
    
    assert active_count == 10

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('simulation-details.csv')


def test_run_sim_decay_lambda_3():

    from infSim.sim import run_sim
    from infSim.settings import make_settings_file
    from infSim.db import create_db

    '''
    In this test the dummy data from lambda two test above is the same as above and now node 4 will not meet the threshold value because of decay on 1 and 3. 
    '''
    
    ## DUMMY DATA ##

    dummy_nodes = list()
    dummy_nodes.append((1,0,3,1))
    dummy_nodes.append((2,2,3,0))
    dummy_nodes.append((3,2,3,0))
    dummy_nodes.append((4,7,3,0))
    dummy_nodes.append((5,5,3,0))
    dummy_nodes.append((6,1,3,0))
    dummy_nodes.append((7,1,3,0))


    dummy_edges = list()
    dummy_edges.append((1,2))
    dummy_edges.append((1,3))
    dummy_edges.append((1,4))
    dummy_edges.append((2,1))
    dummy_edges.append((2,4))
    dummy_edges.append((2,6))
    dummy_edges.append((3,1))
    dummy_edges.append((3,4))
    dummy_edges.append((4,1))
    dummy_edges.append((4,2))
    dummy_edges.append((4,3))
    dummy_edges.append((4,5))
    dummy_edges.append((5,4))
    dummy_edges.append((6,2))
    dummy_edges.append((6,7))
    dummy_edges.append((7,6))

    dummy_active = list()
    dummy_active.append((1,0,3))

    directory_name = os.getcwd()
    
    params = dict(lambda_val=2, decay=1)
    make_settings_file(directory_name, directory_name, params)

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn)

    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?, ?)', dummy_nodes)
    conn.executemany('INSERT INTO edges VALUES (?, ?)', dummy_edges)
    conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', dummy_active)

    conn.commit()

    run_sim(config, conn)

    influenced_nodes = conn.execute('SELECT nodeID FROM nodes WHERE inf=1')

    influenced_count = 0
    for node in influenced_nodes:
        
        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Be Influenced')
        
        influenced_count += 1
    
    assert influenced_count == 6
    
    active_nodes = conn.execute('SELECT * FROM activeNodes')

    active_count=0
    for node in active_nodes:

        if node['nodeID'] == 4:

            if node['round'] != 2 and node['round'] != 3 and node['round'] != 4:

                pytest.fail('Node 4 Should Not Have Been Activated')
        
        if node['nodeID'] == 5:

            pytest.fail('Node 5 Should Not Have Been Activated')
        
        if node['nodeID'] == 1:

            if node['round'] != 0 and node['round'] != 1 and node['round'] != 2:

                pytest.fail('Node 1 Should Only Be Active First and Second Round')
        
        if node['nodeID'] == 3:

            if node['round'] != 1 and node['round'] != 2 and node['round'] !=3:

                pytest.fail('Node 3 Should Only Be Active Second and Third Round')        

        if node['nodeID'] == 2:

            if node['round'] != 1 and node['round'] != 2 and node['round'] !=3:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')

        if node['nodeID'] == 6:

            if node['round'] != 2 and node['round'] != 3 and node['round'] != 4:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')

        if node['nodeID'] == 7:

            if node['round'] != 3 and node['round'] != 4:

                pytest.fail('Node 2 Should Only Be Active Second and Third Round')
        
        active_count += 1
    
    assert active_count == 17

    conn.close()
    os.remove(config['FILES']['DB'])
    os.remove('settings.ini')
    os.remove('simulation-details.csv')