N = [1000,2000,3000,5000];
c = [1,2,3,4,5,6,8,10];
K = 2;
num_reps = 5;
quiet = 0;
len = 10;

ccr_bt = zeros(numel(N),numel(c),num_reps);
ccr_nbt = zeros(numel(N),numel(c),num_reps);
nmi_bt = zeros(numel(N),numel(c),num_reps);
nmi_nbt = zeros(numel(N),numel(c),num_reps);
for i = 1:numel(N)
    for j = 1:numel(c)
        %[G,L] = import_graph_by_edges(N(i),2,c(j),.9,iter);
        [G,L] = sbm_gen(N(i),K,c(j),c(j)/10,45);
        if ~quiet 
                fprintf('N = %d, c = %d\n',N(i),c(j));
        end
        for rep = 1:num_reps
            [~,ccr_bt(i,j,rep),nmi_bt(i,j,rep)] = node_embed_file(G,L,0,len);
            [~,ccr_nbt(i,j,rep),nmi_nbt(i,j,rep)] = node_embed_file(G,L,1,len);
        end
    end
end
save(['figs/nmi_ccr_' datestr(clock,'mm-dd-yy_HH:MM:SS') '.mat'],'nmi_bt','nmi_nbt','ccr_bt','ccr_nbt','N','K','c','len');
for nn = 1:numel(N)
    figure;
    hold on
    yyaxis left
    axis([-inf inf 0 1]);
    errorbar(c,mean(nmi_bt(nn,:,:),3),std(nmi_bt(nn,:,:),0,3))
    errorbar(c,mean(nmi_nbt(nn,:,:),3),std(nmi_nbt(nn,:,:),0,3))
    yyaxis right
    axis([-inf inf 50 100]);
    errorbar(c,mean(ccr_bt(nn,:,:),3),std(ccr_bt(nn,:,:),0,3))
    errorbar(c,mean(ccr_nbt(nn,:,:),3),std(ccr_nbt(nn,:,:),0,3))
    legend({'NMI BT','NMI NBT', 'CCR BT', 'CCR NBT'});
    title(['N = ' num2str(N(nn))]);
    saveas(gcf,sprintf('N%dvariedc.fig',N(nn)));
    saveas(gcf,sprintf('N%dvariedc.png',N(nn)));
end