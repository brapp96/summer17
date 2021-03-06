function E = nodes2edgesgraph(G,doNBT)
profile on;
G = triu(G,1)+triu(G,1)';
n = size(G,1);
row = 0;
indi = [];
indj = [];
inds = {n};
startinds = 1;
endinds = 0;
for i = 1:n
    inds{i} = find(G(i,:));
end
for i = 1:n
    for j = 1:n
        if j == i
            continue;
        end
        row = row + 1;
        % from i to j
        is = inds{j};
        if doNBT
            is(is==i) = [];
        end
        nis = numel(is);
        is(is>=j) = is(is>=j)-1;
        is = is + (n-1)*(j-1);
        endinds = startinds + nis - 1;
        indi(startinds:endinds) = row;
        indj(startinds:endinds) = is;
        startinds = endinds;
    end
end
E = sparse(indi,indj,1,n*(n-1),n*(n-1));
profile viewer;
end