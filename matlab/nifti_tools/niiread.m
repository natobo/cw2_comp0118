% Nifty File Reader
function r=niiread(filename,type)

zipflag=0;
if(findstr(filename(end-1:end),'gz'));
   zipflag=1;
   system(['gunzip ',filename]);
   filename=filename(1:end-3);
end   
r.hdr=load_nii_hdr(filename);
fid=fopen(filename);

fseek(fid,70,'bof');datatype=fread(fid,1,'short');
if(nargin==1);if(datatype==4);type='short';else;type='float';end;end
fseek(fid,42,'bof');ndim=fread(fid,4,'short')';
fseek(fid,80,'bof');vdim=fread(fid,4,'float')';
fseek(fid,352,'bof');V=fread(fid,prod(ndim),type);
r.img=reshape(V,ndim);
fclose(fid);

if(zipflag);
   system(['gzip -f ',filename]);
end
% 
% if(nargin==1);type='float';end
% r=load_nii_hdr(filename);
% vdim=r.dime.dim(2:5);
% pdim=r.dime.pixdim(2:5);
% fid=fopen(filename);
% fseek(fid,352,'bof');
% V=fread(fid,prod(vdim),type);
% V=reshape(V,vdim);
% fclose(fid);