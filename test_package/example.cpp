#include <cstdio>
#include <Urho3D/Urho3D.h>
#include <Urho3D/Engine/Application.h>

int main() {
	auto context = Urho3D::MakeShared<Urho3D::Context>();
	auto application = Urho3D::MakeShared<Urho3D::Application>(context);

	std::puts("package test complete.");
}
