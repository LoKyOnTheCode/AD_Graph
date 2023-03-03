from ldap3 import Connection, Server
from pyvis.network import Network

net = Network(bgcolor="#222222", font_color="white")

domaine = "DC=domain,DC=com"
server = Server('server_ip')
conn = Connection(server, user='DOMAIN_NAME\\username', password='my_password',auto_bind= True)

conn.search(
        search_base=domaine,
        search_filter='(objectClass=organizationalUnit)',
        search_scope='SUBTREE',
        attributes=['ou']
        )

counter = 0
list_ou = []
for entry in conn.entries :
        dn = entry.entry_dn
        OU = dn.split(',')[0]
        OU_parent = dn.split(',')[1]
        net.add_node(OU_parent, label=OU_parent)

        if OU not in list_ou :
                list_ou.append(OU)
                net.add_node(OU, label=OU)
                conn.search(entry.entry_dn, '(objectclass=user)', search_scope='LEVEL', attributes=['cn'])
                for user in conn.entries :
                        u = user.cn.value
                        net.add_node(u, label=u, color="red")
                        net.add_edge(OU, u)
                net.add_edge(OU, OU_parent)
             
        else :
                net.add_node(f"{OU}{counter}", label=OU)
                net.add_edge(f"{OU}{counter}", OU_parent)
                conn.search(entry.entry_dn, '(objectclass=user)', search_scope='LEVEL', attributes=['cn'])
                for user in conn.entries :
                        u = user.cn.value
                        net.add_node(u, label=u, color="red")
                        net.add_edge(f"{OU}{counter}", u)
        
        
        counter += 1
net.show_buttons(filter_="physics")
net.show("my_webpage.html")
conn.unbind()