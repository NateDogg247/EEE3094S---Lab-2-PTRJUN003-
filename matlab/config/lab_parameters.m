function P = lab_parameters()
% One shared parameter file for Python and MATLAB.
projectRoot = fileparts(fileparts(fileparts(mfilename('fullpath'))));
P = jsondecode(fileread(fullfile(projectRoot,'config','lab_parameters.json')));
P.project_root = projectRoot;
end
