r=load_nii('qt2.nii');
size(r.img)
TE=load('TEs.txt')
A=[ones(length(TE),1),TE'];
r.img(r.img(:)<0)=0; % shouldn't be possible!
% "Any voxel intensity that is below 0 is replaced by 0, because negative signal values are not physically expected."
% s=log(r.img);
s=log(double(r.img));

new=A\reshape(s,numel(s)/length(TE),length(TE))';
new(1,:)=exp(new(1,:));

new(2,:)=-1./new(2,:);
new=reshape(new',[size(s,1),size(s,2),size(s,3),2]);

y=squeeze(sum(sum(sum(r.img,1),2),3));
y=y/max(y(:))

% raw data...
y=[1.000	0.983	0.964	0.955	0.932	0.928	0.903	0.863	0.817	0.780	0.748	0.716	0.671	0.634	0.606	0.566	0.504	0.433	0.376	0.327	0.330	0.247]';
TE=[19,20,21,22,23,24,25,28,31,34,37,40,44,48,52,57,67,80,95,110,110,150]';
plot(TE,y,'x-')

% Linear Fitting...
A=[ones(length(TE),1),TE];
p=A\log(y)
T2=-1/p(2)
y1=exp(A*p);
figure;plot(TE,y,'x-',TE,y1,'x-')

% Non-linear fitting...
options=optimset('Display','off');
p2=lsqnonlin(@(p)(y-p(1)*exp(-TE(:)/p(2))),[exp(p(1)),T2],[],[],options)
y2=p2(1)*exp(-TE/p2(2));
figure;plot(TE,y,'x-',TE,y1,'x-',TE,y2,'x-');legend('Data y','Log-Linear','Non-linear');

% Timing data...
tic;
for i=1:1000
    p=A\log(y);
end
disp(['1000 linear fits took ',num2str(toc),'s...'])
tic;
for i=1:1000
    p2=lsqnonlin(@(p)(y-p(1)*exp(-TE(:)/p(2))),[exp(p(1)),T2],[],[],options);
end
disp(['1000 non-linear fits took ',num2str(toc),'s...'])


%This figure is showing a T2 decay curve fit in a biomedical imaging context, most likely MRI relaxometry.