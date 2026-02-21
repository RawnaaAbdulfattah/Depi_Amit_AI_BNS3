mu=398600;
K=[0,0,1];
I=[1,0,0];
%user inputs
r_vec=input('Enter position vector');
v_vec=input('Enter velocity vector');
%determine magnitude for these vectors
r=sqrt(dot(r_vec,r_vec));
v=sqrt(dot(v_vec,v_vec));
%calc specific energy epsilon
epsilon=((v^2)/2)-(mu/r);
fprintf('specific mechanical energy :%f km^2/s^2\n',epsilon);
%semi major axis
a=-mu/(2*epsilon);
fprintf('semi major axis :%f km\n',a);
%find eccentricity vector and it's magnitude
e_vec=((v^2-mu/r)*r_vec-dot(r_vec,v_vec)*v_vec)/mu;
e=sqrt(dot(e_vec,e_vec));
fprintf('eccentricity vector :%f %f %f\n',e_vec);
fprintf('eccentricity magnitude :%f\n',e);
%determine specific angular momentum
h_vec=cross(r_vec,v_vec);
h=sqrt(dot(h_vec,h_vec));
fprintf('specific angular momentum :%f km^2/s\n',h);
%determine inclination
i=acos((dot(K,h_vec))/h);
fprintf('inclination:%f deg\n',i*(180/pi));
%determine n vector
n_vec=cross(K,h_vec);
n=sqrt(dot(n_vec,n_vec));
%determine right ascension of ascending node
if n_vec(2)>=0
    RA=acos(dot(I,n_vec)/n);
else
    RA=360-RA;
end
fprintf('right ascention :%f deg\n',RA*(180/pi));
%determine argument of perigee
if e_vec(3)>=0
    omega=acos(dot(e_vec,n_vec)/(n*e));
else
    omega=360-omega;
end
fprintf('argument of perigee:%f\n',omega*(180/pi));
%determine true anomay
if dot(e_vec,r_vec)>=0
    ta=acos(dot(e_vec,r_vec)/(r*e));
else
    ta=360-ta;
end
fprintf('true anomaly:%f deg\n',ta*(180/pi));

%azimuth velocity
Va=h/r;
fprintf('azimuth velocity :%f km/s\n',Va);
%radial velocity
Vr=(mu/h)*e*sin(ta);
fprintf('radial velocity:%f km/s\n',Vr);
%flight path angle
phi=atan(Vr/Va);
fprintf('flight path angle:%f deg\n',phi*(180/pi));