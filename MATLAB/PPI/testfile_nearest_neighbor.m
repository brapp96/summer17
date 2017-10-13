num_trials = 10;
remove = 50;
neighbors = 10;
weighted = 1;
load('runs/PPIlong.mat');
VECpath = 'MIPS_data/VEC_distance_graph.txt';
if exist('VEC','var')
elseif exist(VECpath,'file')
    VEC = dlmread(VECpath);
else
    VEC = make_distance_graph_from_embeddings(NBT{6},VECpath);
end
if ~exist('DSD','var')
    [DSD,protein_names] = read_DSD_file('MIPS_data/results_converged.DSD1');
end
if ~exist('annos','var') || ~exist('annos_names','var')
    [annos,annos_names] = read_first_level('MIPS_data/MIPSFirstLevel.list');
end

dsd_results_unweighted = zeros(1,num_trials);
dsd_results_weighted = zeros(1,num_trials);
vec_results_unweighted = zeros(1,num_trials);
vec_results_weighted = zeros(1,num_trials);
for ii = 1:num_trials
    dsd_results_unweighted(ii) = nearest_neighbor(DSD,protein_names,annos,annos_names,remove,neighbors,~weighted);
    dsd_results_weighted(ii) = nearest_neighbor(DSD,protein_names,annos,annos_names,remove,neighbors,weighted);
    vec_results_unweighted(ii) = nearest_neighbor(VEC,protein_names,annos,annos_names,remove,neighbors,~weighted);
    vec_results_weighted(ii) = nearest_neighbor(VEC,protein_names,annos,annos_names,remove,neighbors,weighted);
end
figure(1);
clf
plot(dsd_results_unweighted);hold on;plot(vec_results_unweighted);
title('Unweighted');
axis([0 num_trials 0 1]);
legend('DSD','VEC');
figure(2);
clf
plot(dsd_results_weighted);hold on;plot(vec_results_weighted);
title('Weighted');
axis([0 num_trials 0 1]);
legend('DSD','VEC');