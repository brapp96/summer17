% len = [5, 10, 20];
% num_reps = 5;
% BT = cell(numel(len),num_reps);
% NBT = BT;
% [G,~] = import_graph_by_edges(0,0,0);
% for l = 1:numel(len)
%     for rep = 1:num_reps
%         fprintf(1,'length: %d, run: %d\n',len(l),rep);
%         [BT{l,rep},~,~] = node_embed_file(G,0,0,len(l));
%         [NBT{l,rep},~,~] = node_embed_file(G,0,1,len(l));
%     end
% end
% save(['runs/PPI.mat'],'BT','NBT','len');

%%
fp = fopen('PPInames.txt','r');
names = {};
while ~feof(fp)
    names{end+1} = fgetl(fp);
end

%%
k = 43;
Lbt = BT;
Lnbt = BT;
inter = names;
for i = 11:15
    Lbt{i} = kmeans(BT{i},k);
    Lnbt{i} = kmeans(NBT{i},k);
    [~,ind] = sort(hist(Lbt{i},1:k));
    inter = intersect(inter,names(Lbt{i}==ind(end)));
end