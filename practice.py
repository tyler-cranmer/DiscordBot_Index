
newlist = [['#032', 'mel.eth', 'Contribution INFO', 'Yes', 'Link to work', 'Other Notes', 'Time contributed (Hours)', 'Community', 'Sustainability', 'Elliott'], ['#032', 'mel.eth', 'Contribution INFO10', 'Yes', '---', '---', 'Time contributed (Hours)', 'Product', 'Automated Pod', 't'], ['#032', 'mel.eth', 'Contribution INFO2', 'Yes', 'Link to work2', 'Other Notes2', 'Time contributed (Hours)', 'Growth', 'Accountability', 'Elliott'], ['#032', 'mel.eth', 'Contribution INFO3', 'Yes', 'Link to work3', 'Other Notes3', 'Time contributed (Hours)', 'Governance', 'Operational Funding & Payroll', 'ELLIOT'], ['#032', 'mel.eth', 'Contribution INFO4', 'Yes', 'Link to work4', 'Other Notes4', 'Time contributed (Hours)', 'Finance', 'Investment Pod', 'ELLIOT'], ['#032', 'mel.eth', 'Contribution INFO5', 'Yes', 'Link to work5', 'Other Notes5', 'Time contributed (Hours)', 'Product', 'Tokenomics', 'ELLIOT'], ['#032', 'mel.eth', 'Contribution INFO6', 'No', '---', '---', 'Time contributed (Hours)', 'Community', 'Content', 'f'], ['#032', 'mel.eth', 'Contribution INFO7', 'No', '---', '---', 'Time contributed (Hours)', 'Growth', 'Visual & Design', 'p'], ['#032', 'mel.eth', 'Contribution INFO8', 'Yes', '---', '---', 'Time contributed (Hours)', 'Governance', 'Visual & Design', 'f'], ['#032', 'mel.eth', 'Contribution INFO9', 'No', '---', '---', 'Time contributed (Hours)', 'Finance', 'Growth Grants Program', 'g']]
finance_list = []
growth_list = []
community_list = []
product_list = []
governance_list = []
other_list = []
for x in range(len(newlist)):
  if newlist[x][7] == 'Finance':
    finance_list.append(newlist[x])
  elif newlist[x][7] == 'Growth':
    growth_list.append(newlist[x])
  elif newlist[x][7] == 'Governance':
    governance_list.append(newlist[x])
  elif newlist[x][7] == 'Community':
    community_list.append(newlist[x])
  else:
    product_list.append(newlist[x])  

print(f'finance: {finance_list} \n')
print(f'Community: {community_list} \n')
print(f'Growth: {growth_list} \n')
print(f'Governance: {governance_list} \n')
print(f'Poduct: {product_list} \n')