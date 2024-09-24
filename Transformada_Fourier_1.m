clear all

Ts = 0.01;
t = -50:Ts:50;


Tm = 2;
fm = 1/Tm;

x_0 = cos(2*pi*fm*t);

x_1 = rectpuls(t,1);
x_2 = rectpuls(t,2);
x_3 = tripuls(t,2);

Nt = length(t);
f = linspace(-0.5,0.5,Nt)*(1/Ts);


Y_0 = fft(x_0);
X_0 = fftshift(Y_0);
tol = 1e-6;
X_0(abs(X_0) < tol) = 0;

theta_0 = angle(X_0);

Y_1 = fft(x_1);
Y_2 = fft(x_2);
Y_3 = fft(x_3);

X_1 = fftshift(Y_1);
X_2 = fftshift(Y_2);
X_3 = fftshift(Y_3);

% tol = 1e-6;
% X_1(abs(X_1) < tol) = 0;
% theta_1 = angle(X_1);
% 
% tol = 1e-6;
% X_2(abs(X_2) < tol) = 0;
% theta_2 = angle(X_2);
% 
% % tol = 10;
% % X_3(abs(X_3) < tol) = 0;
% theta_3 = angle(X_3);

figure(10)
subplot(211)
plot(t,x_0,'k')
grid on
axis([-5 5 -1 1])
subplot(212)
plot(t,x_1,'r',...
     t,x_2,'b',...
     t,x_3,'m','LineWidth',2)
grid on
axis([-5 5 0 1.2])

figure(20)
stem(f,abs((X_0)),'k')
grid on

figure(30)
plot(f,abs((X_1)),'k')
grid on
axis([-10 10 0 1e2])

figure(40)
plot(f,abs((X_2)),'k',...
     f,abs((X_1)),'b')
grid on
axis([-10 10 0 2e2])

figure(50)
plot(f,abs(X_3),'k')
grid on
axis([-10 10 0 1e2])







